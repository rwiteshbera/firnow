import re
from datetime import datetime
from typing import Annotated, TypeVar

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from pydantic.functional_validators import AfterValidator
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from models.auth import AccessToken
from models.tables import PoliceStation

# Pattern to match the password with atleast one uppercase, one lowercase,
# one digit and one special character.
password_pattern = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?])")


def check_length(password: str) -> str:
    if not 8 <= len(password) <= 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password must be atleast 8 characters long.",
            },
        )
    return password


def check_password(password: str) -> str:
    if not bool(password_pattern.match(password)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password must contain atleast one uppercase, one lowercase, one digit and one special character.",
            },
        )
    return password


PasswordType = Annotated[
    str, AfterValidator(check_length), AfterValidator(check_password)
]


class PoliceStationRequest(
    pydantic_model_creator(
        PoliceStation,
        name="PoliceStationRequest",
        include=("name", "email", "state", "district"),
        sort_alphabetically=True,
    )
):
    email: EmailStr
    password: PasswordType


class PoliceStation_Pydantic(
    pydantic_model_creator(
        PoliceStation,
        name="PoliceStation_Pydantic",
        exclude=("password",),
        sort_alphabetically=True,
    )
):
    model_config = ConfigDict(populate_by_name=True)
    email: EmailStr
    updated_at: datetime = Field(..., alias="updatedAt")


class PoliceStationResponse(AccessToken):
    redirect: HttpUrl


class PoliceStationRegistrationResponse(PoliceStationResponse):
    police_station: PoliceStation_Pydantic
