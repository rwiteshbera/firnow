from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, HttpUrl
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from models.auth import AccessToken
from models.tables import PoliceStation
from utils.validators import PasswordType


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


class PoliceStationSearched_Pydantic(
    pydantic_model_creator(
        PoliceStation,
        name="PoliceStationSearched_Pydantic",
        exclude=("password", "email", "updated_at", "verified"),
        sort_alphabetically=True,
    )
):
    pass


class PoliceStationResponse(AccessToken):
    redirect: HttpUrl


class PoliceStationRegistrationResponse(PoliceStationResponse):
    police_station: PoliceStation_Pydantic
