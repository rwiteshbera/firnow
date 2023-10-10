from datetime import datetime, timedelta

from jose import jwt

from config import settings


def create_token(data: dict, expire_delta: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=expire_delta)
    to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
