from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import FilePath, HttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Mode(Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )

    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    APP_CREATION_DATE: datetime = datetime(2021, 1, 1)
    APP_HOST: HttpUrl = HttpUrl("http://127.0.0.1:8000")
    FIRESTORE_CERT: FilePath = Path("cert.json")
    INTERNAL_ID_SERVER: HttpUrl = HttpUrl(f"{APP_HOST}id")
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = (
        "37401a016623f5f320bda74c83063d32ebc4bf5417bd5dbf99aa4f0afbf4cb02"
    )
    MODE: Mode = Mode.PROD
    NODE_ID: int = 0
    POSTGRES_URL: PostgresDsn = PostgresDsn(
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    REDIS_URL: RedisDsn = RedisDsn("redis://username:password@localhost:6379")
    REFRESH_TOKEN_EXPIRE_HOURS: int = 72
    WEB3_STORAGE_TOKEN: str = ""

    @field_validator("APP_CREATION_DATE", mode="before")
    @classmethod
    def parse_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, "%d-%m-%Y")

        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY format.")

    @field_validator("WEB3_STORAGE_TOKEN", mode="before")
    @classmethod
    def parse_web3_storage_token(cls, value: str) -> str:
        if value:
            return value
        raise ValueError("WEB3_STORAGE_TOKEN is required.")


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=2))
