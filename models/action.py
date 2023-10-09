from typing import Optional

from pydantic import BaseModel, HttpUrl


class OTPAction(BaseModel):
    sendOtp: Optional[HttpUrl] = None
    verifyOtp: Optional[HttpUrl] = None
