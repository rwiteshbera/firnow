from contextlib import asynccontextmanager
from typing import Optional

from aiohttp import ClientSession
from fastapi import FastAPI

from databases.postgres import PostgresSession
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
    await PostgresSession.init()
    await Mailer.get_client()
    yield
    await SingletonSession.close_session()
    await PostgresSession.close()
    await RedisClient.close_client()
    await Mailer.close_client()
