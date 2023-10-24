from contextlib import asynccontextmanager
from typing import Optional

from aiohttp import ClientSession
from fastapi import FastAPI
from tortoise import Tortoise

from config import settings
from databases.redis import RedisClient
from utils.mail import Mailer


class SingletonSession:
    _session: Optional[ClientSession] = None

    @classmethod
    def get_session(cls) -> ClientSession:
        if cls._session is None:
            cls._session = ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls) -> None:
        if cls._session is not None:
            await cls._session.close()
            cls._session = None


@asynccontextmanager
async def init(app: FastAPI):
    SingletonSession.get_session()
    await RedisClient.get_client()
    await Tortoise.init(
        db_url=str(settings.POSTGRES_URL),
        modules={"models": ["models.tables"]},
        use_tz=True,
    )
    await Tortoise.generate_schemas()
    await Mailer.get_client()
    yield
    await SingletonSession.close_session()
    await Tortoise.close_connections()
    await RedisClient.close_client()
    await Mailer.close_client()
