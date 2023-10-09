from aiohttp import ClientSession

from session import SingletonSession
from settings import config


async def get_id() -> int:
    session: ClientSession = SingletonSession.get_session()
    id_server_url: str = config["INTERNAL_ID_SERVER"] or "http://127.0.0.1:8000/id"

    async with session.get(id_server_url) as resp:
        snowflake = await resp.json()
        id = snowflake["snowflake"]

    return id
