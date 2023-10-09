from datetime import datetime, timedelta

from jose import jwt

from settings import config

SECRET_KEY = (
    config["JWT_SECRET_KEY"]
    or "37401a016623f5f320bda74c83063d32ebc4bf5417bd5dbf99aa4f0afbf4cb02"
)
ALGORITHM = config["JWT_ALGORITHM"] or "HS256"


def create_token(data: dict, expire_delta: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=expire_delta)
    to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
