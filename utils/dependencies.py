import asyncio
from typing import Annotated, Any, Optional, cast

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from config import settings
from models.police_station import PoliceStation_Pydantic
from models.tables import PoliceStation
from routes.police_station_urls import LOGIN_URL

oauth2_scheme_police = OAuth2PasswordBearer(tokenUrl="police-station/login")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="user/login")


def get_refresh_token(
    refresh_token: Annotated[Optional[str], Cookie()] = None
) -> Optional[str]:
    return refresh_token


async def get_id_from_token(
    refresh_token: Annotated[Optional[str], Depends(get_refresh_token)]
) -> int:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Failed to retrieve the refresh token",
                "redirect": str(LOGIN_URL),
            },
        )

    return await get_id(refresh_token)


async def get_id(token: str) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Could not validate credentials",
            "redirect": str(LOGIN_URL),
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = await asyncio.to_thread(
            jwt.decode,
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("id", 0)

    except JWTError:
        raise credentials_exception


async def get_police_station_id(
    token: Annotated[str, Depends(oauth2_scheme_police)]
) -> int:
    return await get_id(token)


async def get_user_id(token: Annotated[str, Depends(oauth2_scheme_user)]) -> int:
    return await get_id(token)


async def get_police_station(
    id: Annotated[int, Depends(get_police_station_id)]
) -> PoliceStation:
    try:
        police_station = await PoliceStation.get(id=id)
        return cast(
            PoliceStation,
            await PoliceStation_Pydantic.from_tortoise_orm(police_station),
        )

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Police Station not found",
            },
        )


# async def get_user(id: Annotated[int, Depends(get_user_id)]) -> User_Pydantic:
#     ...
