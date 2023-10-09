from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from models.action import OTPAction


class OTPRequest(BaseModel):
    otp: str


class OTPResponse(BaseModel):
    message: str


class OTPSentResponse(OTPResponse):
    actions: OTPAction


class OTPVerifiedResponse(OTPResponse):
    redirect: HttpUrl


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refreshAfter: float
    refreshUrl: HttpUrl


class Snowflake(BaseModel):
    snowflake: int
