import asyncio
from typing import Annotated, Any, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from models.police_station import PoliceStation_Pydantic
from models.tables import PoliceStation
from settings import config

oauth2_scheme_police = OAuth2PasswordBearer(tokenUrl="police-station/login")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="user/login")
HOST: str = config["APP_HOST"] or "http://127.0.0.1:8000"
SECRET_KEY = (
    config["JWT_SECRET_KEY"]
    or "37401a016623f5f320bda74c83063d32ebc4bf5417bd5dbf99aa4f0afbf4cb02"
)
ALGORITHM = config["JWT_ALGORITHM"] or "HS256"


async def get_id(token: str, for_: str) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Could not validate credentials",
            "redirect": f"{HOST}/auth/{for_}/login",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = await asyncio.to_thread(
            jwt.decode,
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload.get("id", 0)

    except JWTError:
        raise credentials_exception


async def get_police_station_id(
    token: Annotated[str, Depends(oauth2_scheme_police)]
) -> int:
    return await get_id(token, "police-station")


async def get_user_id(token: Annotated[str, Depends(oauth2_scheme_user)]) -> int:
    return await get_id(token, "user")


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
