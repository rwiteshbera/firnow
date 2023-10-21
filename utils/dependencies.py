import asyncio
from typing import Annotated, Optional, cast

from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import validator
from requests import head
from starlette.requests import ClientDisconnect
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.validators import MaxSizeValidator, ValidationError
from tortoise.exceptions import DoesNotExist

from config import settings
from models.errors import InvalidFileException, MaxBodySizeException
from models.police_station import PoliceStation_Pydantic
from models.tables import PoliceStation
from models.upload_file import TemporaryUploadFile
from routes.police_station_urls import LOGIN_URL

oauth2_scheme_police = OAuth2PasswordBearer(tokenUrl="police-station/login")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="user/login")


def get_refresh_token(
    refresh_token: Annotated[Optional[str], Cookie()] = None
) -> Optional[str]:
    """
    Get refresh token from cookie.
    """
    return refresh_token


async def get_id_from_token(
    refresh_token: Annotated[Optional[str], Depends(get_refresh_token)]
) -> int:
    """
    Extract id from refresh token. This function depends on the refresh
    token to be fetched from the cookie.
    """
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
    """
    Extract ID from the token.

    Params
    ------
      token: str: The token from which the ID is to be extracted.

    Returns
    -------
      int: The ID extracted from the token.
    """
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


async def get_file(request: Request) -> TemporaryUploadFile:
    try:
        size_validator = MaxSizeValidator(max_size=5 * 1024 * 1024)
        file = TemporaryUploadFile(validator=size_validator)
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", file)

        async for chunk in request.stream():
            parser.data_received(chunk)

        if file.content_type != "application/pdf":
            raise InvalidFileException

        return file

    except ClientDisconnect:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Client disconnected while uploading the file",
            },
        )

    except (MaxBodySizeException, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "message": "Maximum file size limit (5 MB) exceeded",
            },
        )

    except InvalidFileException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Only PDF files are allowed.",
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "There was an error uploading the file",
            },
        )
