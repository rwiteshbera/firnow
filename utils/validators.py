from typing import Annotated

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic.functional_validators import AfterValidator

from models.errors import MaxBodySizeException
from utils.password import password_pattern


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


class MaxBodySizeValidator:
    def __init__(self, max_body_size: int):
        self.body_len = 0
        self.max_size = max_body_size

    def __call__(self, chunk: bytes):
        self.body_len += len(chunk)
        if self.body_len > self.max_size:
            raise MaxBodySizeException(body_len=self.body_len)
