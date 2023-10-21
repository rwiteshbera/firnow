import hashlib
import os
import re
from base64 import b64decode, b64encode

# Pattern to match the password with atleast one uppercase, one lowercase,
# one digit and one special character.
password_pattern = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?])")


def encrypt(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = os.urandom(64)
    hashed = hashlib.scrypt(password_bytes, salt=salt, n=16384, r=8, p=1, dklen=128)
    return f"{b64encode(salt).decode('utf-8')}.{b64encode(hashed).decode('utf-8')}"


def verify_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split(".")
    salt = b64decode(salt.encode("utf-8"))
    hashed = b64decode(hashed.encode("utf-8"))
    hashed_password_bytes = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=16384, r=8, p=1, dklen=128
    )
    return hashed_password_bytes == hashed
