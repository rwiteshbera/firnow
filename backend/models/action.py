from typing import Optional

from pydantic import BaseModel, HttpUrl


class SentOtp(BaseModel):
    verifyOtp: HttpUrl


class InvalidOtp(BaseModel):
    sendOtp: HttpUrl
