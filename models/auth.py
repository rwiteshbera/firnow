from pydantic import BaseModel, ConfigDict, HttpUrl
from pydantic.alias_generators import to_camel

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
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    access_token: str
    token_type: str = "bearer"
    refresh_after: float
    refresh_url: HttpUrl


class Snowflake(BaseModel):
    snowflake: int
