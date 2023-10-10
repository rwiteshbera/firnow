from pydantic import BaseModel, HttpUrl

from models.action import InvalidOtp, SentOtp


class OtpRequest(BaseModel):
    otp: str


class OtpResponse(BaseModel):
    message: str


class SentOtpResponse(OtpResponse):
    action: SentOtp


class InvalidOtpResponse(OtpResponse):
    action: InvalidOtp


class VerifiedOtpResponse(OtpResponse):
    redirect: HttpUrl


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refreshAfter: float
    refreshUrl: HttpUrl


class Snowflake(BaseModel):
    snowflake: int
