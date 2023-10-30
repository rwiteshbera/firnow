from typing import Optional

from tortoise import Tortoise
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.connection import connections

from config import settings


class PostgresSession:
    _conn: Optional[BaseDBAsyncClient] = None

    @classmethod
    async def init(cls) -> None:
        if cls._conn:
            return
        await Tortoise.init(
            db_url=str(settings.POSTGRES_URL),
            modules={"models": ["models.tables"]},
            use_tz=True,
        )
        cls._conn = connections.get("default")
        await Tortoise.generate_schemas()

    @classmethod
    async def close(cls) -> None:
        if not cls._conn:
            return
        await Tortoise.close_connections()
        cls._conn = None
