import asyncio
from typing import Annotated, Any, Optional, cast

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import HttpUrl

from databases.redis import RedisClient
from models.auth import (
    AccessToken,
    OTPAction,
    OTPRequest,
    OTPSentResponse,
    OTPVerifiedResponse,
)
from models.errors import PoliceStationNotFound
from models.police_station import (
    PoliceStation_Pydantic,
    PoliceStationRegistrationResponse,
    PoliceStationRequest,
    PoliceStationResponse,
)
from models.tables import PoliceStation
from settings import config
from utils.dependencies import get_police_station
from utils.id import get_id
from utils.otp import generate_otp, send_otp
from utils.password import encrypt, verify_password
from utils.token import create_token

router = APIRouter(prefix="/police-station", tags=["Police Station"])

ACCESS_TOKEN_EXPIRE_HOURS: int = int(config["ACCESS_TOKEN_EXPIRE_HOURS"] or 24)
REFRESH_TOKEN_EXPIRE_HOURS: int = int(config["REFRESH_TOKEN_EXPIRE_HOURS"] or 24 * 7)
HOST: str = config["APP_HOST"] or "http://127.0.0.1:8000"


async def authenticate_police(email: str, password: str) -> Optional[PoliceStation]:
    police_station = await PoliceStation.get_or_none(email=email)
    if police_station is None:
        raise PoliceStationNotFound

    matched = await asyncio.to_thread(
        verify_password, password, police_station.password
    )
    return police_station if matched else None


@router.post("/register", response_model=PoliceStationRegistrationResponse)
async def register_police_station(response: Response, payload: PoliceStationRequest):
    # check if the email id already exists
    if await PoliceStation.exists(email=payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Police Station already exists",
                "redirect": f"{HOST}/auth{router.prefix}/login",
            },
        )

    id = await get_id()
    police_station_req = payload.model_dump(exclude_unset=True)
    police_station_req["id"] = id
    police_station_req["password"] = await asyncio.to_thread(
        encrypt, police_station_req["password"]
    )
    result = await PoliceStation.create(**police_station_req)

    police_station_resp = await PoliceStation_Pydantic.from_tortoise_orm(result)
    access_token = await asyncio.to_thread(
        create_token,
        {"id": result.id},
        ACCESS_TOKEN_EXPIRE_HOURS,
    )
    refresh_token = await asyncio.to_thread(
        create_token,
        {"access_token": access_token},
        ACCESS_TOKEN_EXPIRE_HOURS * 24,
    )
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    access_token_obj = AccessToken(
        access_token=access_token,
        refreshAfter=ACCESS_TOKEN_EXPIRE_HOURS - 0.5,
        refreshUrl=HttpUrl(f"{HOST}/auth/refresh"),
    )

    otp_resp = await send_otp(f"{HOST}/auth{router.prefix}/send-otp", access_token)
    url = otp_resp.actions.verifyOtp or HttpUrl(
        f"{HOST}/auth{router.prefix}verify-email"
    )

    return PoliceStationRegistrationResponse(
        **access_token_obj.model_dump(),
        police_station=cast(PoliceStation_Pydantic, police_station_resp),
        redirect=url,
    )


@router.post("/login", response_model=PoliceStationResponse)
async def login_police_station(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        police_station = await authenticate_police(
            form_data.username, form_data.password
        )

        if police_station is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Incorrect email or password.",
                },
            )

        access_token = await asyncio.to_thread(
            create_token,
            {"id": police_station.id},
            ACCESS_TOKEN_EXPIRE_HOURS,
        )
        refresh_token = await asyncio.to_thread(
            create_token,
            {"access_token": access_token},
            ACCESS_TOKEN_EXPIRE_HOURS * 24,
        )
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        access_token_obj = AccessToken(
            access_token=access_token,
            refreshAfter=ACCESS_TOKEN_EXPIRE_HOURS - 0.5,
            refreshUrl=HttpUrl(f"{HOST}/auth/refresh"),
        )
        successful_resp = PoliceStationResponse(
            **access_token_obj.model_dump(),
            redirect=HttpUrl(f"{HOST}{router.prefix}/dashboard"),
        )

        if not police_station.verified:
            otp_resp = await send_otp(
                f"{HOST}/auth{router.prefix}/send-otp", access_token
            )

            if url := otp_resp.actions.verifyOtp:
                successful_resp.redirect = url

            return successful_resp

        return successful_resp

    except PoliceStationNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Email ID not found.",
                "redirect": f"{HOST}/auth{router.prefix}/register",
            },
        )


@router.get(
    "/send-otp",
    response_model=OTPSentResponse,
    response_model_exclude_unset=True,
)
async def send_otp_police_station(
    unverified: Annotated[PoliceStation, Depends(get_police_station)]
):
    otp = generate_otp(6)
    # send otp to email
    redis = RedisClient.get_client()
    await redis.set(f"otp:{unverified.id}", otp, ex=60 * 5)  # type: ignore
    return OTPSentResponse(
        message="OTP sent successfully",
        actions=OTPAction(
            verifyOtp=HttpUrl(f"{HOST}/auth{router.prefix}/verify-email")
        ),
    )


@router.post(
    "/verify-email",
    response_model=OTPVerifiedResponse,
)
async def verify_police_station_email(
    unverified: Annotated[PoliceStation, Depends(get_police_station)],
    body: OTPRequest,
):
    if unverified.verified:  # type: ignore
        return OTPVerifiedResponse(
            message="Email already verified",
            redirect=HttpUrl(f"{HOST}{router.prefix}/dashboard"),
        )

    detail = OTPSentResponse(
        message="Invalid OTP",
        actions=OTPAction(sendOtp=HttpUrl(f"{HOST}/auth{router.prefix}/send-otp")),
    )

    otp_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=jsonable_encoder(detail, exclude_unset=True),
    )
    redis = RedisClient.get_client()
    otp = await redis.get(f"otp:{unverified.id}")

    if not otp:
        detail.message = "OTP expired"
        raise otp_error

    if otp == body.otp:
        await redis.delete(f"otp:{unverified.id}")
        await PoliceStation.select_for_update().filter(id=unverified.id).update(
            verified=True
        )
        return OTPVerifiedResponse(
            message="Email verified successfully",
            redirect=HttpUrl(f"{HOST}{router.prefix}/dashboard"),
        )

    raise otp_error
