import asyncio
from typing import Annotated, Optional, cast

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from databases.redis import RedisClient
from models.auth import (
    InvalidOtp,
    InvalidOtpResponse,
    OtpRequest,
    SentOtp,
    SentOtpResponse,
    VerifiedOtpResponse,
)
from models.errors import (
    PoliceStationNotFound,
    RequestError,
    RequestErrorWithAction,
    RequestErrorWithRedirect,
)
from models.police_station import (
    PoliceStation_Pydantic,
    PoliceStationRegistrationResponse,
    PoliceStationRequest,
    PoliceStationResponse,
)
from models.tables import PoliceStation
from routes.police_station_urls import *
from utils.dependencies import get_police_station
from utils.id import get_id
from utils.otp import generate_otp, send_otp
from utils.password import encrypt, verify_password
from utils.token import get_access_token_obj

router = APIRouter(
    prefix=f"/{prefix}", tags=["Police Station Authentication Endpoints"]
)

ACCESS_TOKEN_EXPIRE_HOURS: int = settings.ACCESS_TOKEN_EXPIRE_HOURS
REFRESH_TOKEN_EXPIRE_HOURS: int = settings.REFRESH_TOKEN_EXPIRE_HOURS


async def authenticate_police(email: str, password: str) -> Optional[PoliceStation]:
    police_station = await PoliceStation.get_or_none(email=email)
    if police_station is None:
        raise PoliceStationNotFound

    matched = await asyncio.to_thread(
        verify_password, password, police_station.password
    )
    return police_station if matched else None


@router.post(
    "/register",
    summary="Register a new police station",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successful Response",
            "model": PoliceStationRegistrationResponse,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflict Error",
            "model": RequestErrorWithRedirect,
        },
    },
)
async def register_police_station(
    response: Response, payload: Annotated[PoliceStationRequest, Body()]
):
    """
    Register a new police station. The request body should contain the following fields:
    - **name:** Name of the police station
    - **email:** Email ID of the police station
    - **password:** Password to be set for the police station
    - **state:** Name of the state where the police station is located
    - **district:** Name of the district where the police station is located

    **Example:**
    ```
    {
        "name": "Example Thana",
        "email": "example.thana@gov.in",
        "password": "1234567Aa@",
        "state": "West Bengal",
        "district": "Hooghly"
    }
    ```
    """
    # check if the email id already exists
    if await PoliceStation.exists(email=payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Police Station already exists",
                "redirect": str(LOGIN_URL),
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
    access_token_obj = await get_access_token_obj(result.id, response)

    otp_resp = await send_otp(SEND_OTP_URL, access_token_obj.access_token)

    return PoliceStationRegistrationResponse(
        **access_token_obj.model_dump(),
        police_station=cast(PoliceStation_Pydantic, police_station_resp),
        redirect=otp_resp.action.verifyOtp,
    )


@router.post(
    "/login",
    summary="Login to an existing police station account",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "model": PoliceStationResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized Response",
            "model": RequestError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": RequestErrorWithRedirect,
        },
    },
)
async def login_police_station(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login to an existing police station account. The request payload should be sent as a
    form data with the following fields:
    - **username:** Email ID of the police station
    - **password:** Password of the police station

    The `accessToken` received in the response should be used as a ***bearer token*** while making
    request to the protected endpoints.
    """
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
        access_token_obj = await get_access_token_obj(police_station.id, response)
        successful_resp = PoliceStationResponse(
            **access_token_obj.model_dump(),
            redirect=POLICE_STATION_DASHBOARD_URL,
        )

        if not police_station.verified:
            otp_resp = await send_otp(SEND_OTP_URL, access_token_obj.access_token)
            successful_resp.redirect = otp_resp.action.verifyOtp
            return successful_resp

        return successful_resp

    except PoliceStationNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Email ID not found.",
                "redirect": str(REGISTER_URL),
            },
        )


@router.post(
    "/verify-email",
    summary="Verify the police station email",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "model": VerifiedOtpResponse,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid OTP Response",
            "model": RequestErrorWithAction,
        },
    },
)
async def verify_police_station_email(
    unverified: Annotated[PoliceStation, Depends(get_police_station)],
    body: OtpRequest,
):
    """
    Verify the police station email. The request body should contain the following fields:
    - **otp:** OTP sent to the police station email

    **Example:**
    ```
    {
        "otp": "123456"
    }
    ```
    """
    if unverified.verified:
        return VerifiedOtpResponse(
            message="Email already verified",
            redirect=POLICE_STATION_DASHBOARD_URL,
        )

    detail = InvalidOtpResponse(
        message="Invalid OTP",
        action=InvalidOtp(sendOtp=SEND_OTP_URL),
    )

    redis = await RedisClient.get_client()
    otp = await redis.get(f"otp:{unverified.id}")

    if not otp:
        detail.message = "OTP expired"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(detail, exclude_unset=True),
        )

    if otp == body.otp:
        await redis.delete(f"otp:{unverified.id}")
        await PoliceStation.select_for_update().filter(id=unverified.id).update(
            verified=True
        )
        return VerifiedOtpResponse(
            message="Email verified successfully",
            redirect=POLICE_STATION_DASHBOARD_URL,
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=jsonable_encoder(detail, exclude_unset=True),
    )


@router.get(
    "/send-otp",
    summary="Send OTP to the police station email",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "model": SentOtpResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized Response",
            "model": RequestErrorWithRedirect,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": RequestError,
        },
    },
)
async def send_otp_police_station(
    unverified: Annotated[PoliceStation, Depends(get_police_station)]
):
    """
    Send OTP to the email address associated with the police-station account.
    This is a protected endpoint and requires the `accessToken` to be sent as a ***bearer token***.
    """
    otp = generate_otp(6)
    # send otp to email
    redis = await RedisClient.get_client()
    await redis.set(f"otp:{unverified.id}", otp, ex=60 * 5)
    return SentOtpResponse(
        message="OTP sent successfully",
        action=SentOtp(verifyOtp=VERIFY_EMAIL_URL),
    )
