from typing import Optional

import redis.asyncio as redis

from settings import config


class RedisClient:
    _db: Optional[redis.Redis] = None
    _host: str = config["REDIS_HOST"] or "localhost"
    _port: int = int(config["REDIS_PORT"] or 6379)
    _password: Optional[str] = config["REDIS_PASSWORD"]

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._db is None:
            cls._db = redis.Redis(
                host=cls._host,
                port=cls._port,
                password=cls._password,
                protocol=3,
                decode_responses=True,
            )
        return cls._db

    @classmethod
    async def close_client(cls):
        if cls._db is not None:
            await cls._db.close()
            cls._db = None
