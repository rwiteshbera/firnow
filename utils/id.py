from aiohttp import ClientSession

from session import SingletonSession
from config import settings


async def get_id() -> int:
    session: ClientSession = SingletonSession.get_session()
    id_server_url: str = str(settings.INTERNAL_ID_SERVER)

    async with session.get(id_server_url) as resp:
        snowflake = await resp.json()
        id = snowflake["snowflake"]

    return id
