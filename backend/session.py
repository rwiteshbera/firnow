from typing import Optional

from aiohttp import ClientSession


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
