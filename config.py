from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import (
    EmailStr,
    Field,
    FilePath,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Mode(Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    APP_HOST: HttpUrl = HttpUrl("https://firnow.ducksdns.org")
    APP_CREATION_DATE: datetime = datetime(2021, 1, 1)
    API_HOST: HttpUrl = HttpUrl("http://127.0.0.1:8000")
    FIRESTORE_CERT: FilePath = Path("cert.json")
    INTERNAL_ID_SERVER: HttpUrl = HttpUrl(f"http://127.0.0.1:8002/")
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
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 456
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    TEST_EMAIL: EmailStr = "test@example.com"
    WEB3_STORAGE_TOKEN: str = ""
    UVICORN_WORKERS: int = Field(default=1, validate_default=True)

    @property
    def ACCESS_LOG(self) -> bool:
        return True if self.MODE == Mode.DEV else False

    @property
    def LOG_LEVEL(self) -> str:
        return "debug" if self.MODE == Mode.DEV else "info"

    @field_validator("UVICORN_WORKERS", mode="after")
    def validate_uvi_workers(cls, value, info: ValidationInfo) -> int:
        if info.data["MODE"] == Mode.DEV:
            return 1
        return value

    @field_validator("APP_CREATION_DATE", mode="before")
    @classmethod
    def parse_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, "%d-%m-%Y")

        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY format.")

    @field_validator(
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "WEB3_STORAGE_TOKEN",
        mode="before",
    )
    @classmethod
    def parse_web3_storage_token(cls, value: str) -> str:
        if value:
            return value
        raise ValueError("Value required to be set.")


settings = Settings()


def get_log_config(filename: str):
    log_config = {
        "version": 1.0,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": f"logs/{filename}.log",
                "formatter": "default",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": settings.LOG_LEVEL.upper(),
            },
        },
    }
    return log_config


if __name__ == "__main__":
    print(settings.model_dump_json(indent=2))
