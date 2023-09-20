import asyncio
from typing import cast

import aiohttp
from aiohttp import ClientSession

from firebase.firestore import db
from utils.scrap import get_districts, get_states


async def populate_states(session: ClientSession) -> None:
    """
    Insert all the states of India in the database.

    Args:
        session (ClientSession): `aiohttp` session

    Returns:
        None
    """
    states = await get_states(session)
    for state in states:
        await db.collection("states").document(state["code"]).set(state)


async def populate_districts(session: ClientSession) -> None:
    """
    Insert all the districts of Indian states in the database.

    Args:
        session (ClientSession): `aiohttp` session

    Returns:
        None
    """
    districts = await get_districts(session)
    for k, v in districts.items():
        await db.collection("districts").document(k).set(cast(dict, v))


if __name__ == "__main__":

    async def main():
        states = await db.collection("states").get()  # type: ignore
        districts = await db.collection("districts").get()  # type: ignore

        async with aiohttp.ClientSession() as session:
            tasks = []

            if not states:
                tasks.append(asyncio.create_task(populate_states(session)))

            if not districts:
                tasks.append(asyncio.create_task(populate_districts(session)))

            await asyncio.gather(*tasks)

    asyncio.run(main())
