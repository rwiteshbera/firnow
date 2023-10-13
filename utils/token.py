import asyncio
from datetime import datetime, timedelta

from fastapi import Response
from jose import jwt

from config import settings
from models.auth import AccessToken
from routes.police_station_urls import REFRESH_TOKEN_URL


async def get_access_token_obj(id: int, response: Response) -> AccessToken:
    """
    This function is used to set cookie and get `access_token_obj`.

    Params
    ------
        id: int: ID to be encoded in JWT
        response: fastapi.Response: Fastapi response object

    Return
    ------
        Returns access token object
    """
    access_token = await asyncio.to_thread(
        create_token,
        {"id": id},
        settings.ACCESS_TOKEN_EXPIRE_HOURS,
    )
    refresh_token = await asyncio.to_thread(
        create_token,
        {"id": id},
        settings.ACCESS_TOKEN_EXPIRE_HOURS * 24,
    )
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    access_token_obj = AccessToken(
        access_token=access_token,
        refresh_after=get_expire_time(settings.ACCESS_TOKEN_EXPIRE_HOURS - 0.5),
        refresh_url=REFRESH_TOKEN_URL,
    )

    return access_token_obj


def get_expire_time(hours: float) -> datetime:
    """
    Get expire time.

    Params
    ------
        hours: float: Number of hours to set as an offset to current time.

    Return
    ------
        Returns time as datetime object.
    """
    return datetime.utcnow() + timedelta(hours=hours)


def create_token(data: dict, expire_delta: int) -> str:
    """
    Create JWT token taking data to be encoded and offset to the current
    time (in hours) until when the token is valid.

    Params
    ------
        data: dict: Data to be encoded in JWT
        expire_delta: int: Number of hours to set as an offset to current time.

    Return
    ------
        Returns JWT token as string.
    """
    expire = get_expire_time(hours=expire_delta)
    to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
