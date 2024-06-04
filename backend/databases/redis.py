import asyncio
from typing import Optional

import redis.asyncio as redis

from config import settings


class RedisClient:
    _db: Optional[redis.Redis] = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        if cls._db is None:
            # cls._db = redis.Redis(
            #     host=cls._host,
            #     port=cls._port,
            #     password=cls._password,
            #     protocol=3,
            #     decode_responses=True,
            # )
            cls._db = await redis.from_url(
                str(settings.REDIS_URL),
                protocol=3,
                decode_responses=True,
            )

        return cls._db

    @classmethod
    async def close_client(cls):
        if cls._db is not None:
            await cls._db.close()
            cls._db = None
