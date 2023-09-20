import asyncio
import json
import re
from typing import TypedDict

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup, SoupStrainer

District = TypedDict("District", {"districts": list[str], "total": int})


async def get_states(
    session: ClientSession,
    url: str = "https://en.wikipedia.org/wiki/States_and_union_territories_of_India",
) -> list[dict[str, str]]:
    """
    Scrap list of all states in India from Wikipedia.

    Args:
        session (ClientSession): `aiohttp` session
        url (str): URL to scrap from. Here Wikipedia.

    Returns:
        (list[dict[str, str]]): List of states and their codes.
    """
    result: str = await get_response(session, url)
    tables = SoupStrainer("table", class_="wikitable sortable plainrowheaders")
    soup = BeautifulSoup(result, "lxml", parse_only=tables)
    states: list[dict[str, str]] = []

    for table in soup.find_all("table"):
        for row in table.find_all("tr")[1:]:
            state, code = row.find_all(["th", "td"])[:2]
            state, code = state.text.strip(), code.text.strip()
            states.append({"name": state, "code": code, "country": "IN"})

    return sorted(states, key=lambda x: x["name"])


async def get_districts(
    session: ClientSession,
    url: str = "https://en.wikipedia.org/wiki/List_of_districts_in_India",
) -> dict[str, District]:
    """
    Scrap list of all districts in India from Wikipedia.

    Args:
        session (ClientSession): `aiohttp` session
        url (str): url to scrap from. Here Wikipedia.

    Returns:
        (dict[str, District]): Dictionary of states and their districts.
    """
    result: str = await get_response(session, url)
    states = SoupStrainer("h3")
    tables = SoupStrainer("table", class_="wikitable sortable")
    states = BeautifulSoup(result, "lxml", parse_only=states).select(
        "h3 > span + .mw-headline"
    )
    tables = BeautifulSoup(result, "lxml", parse_only=tables).find_all("table")[1:]
    dist = {}
    patt = re.compile(r"[\w ]+")

    for state, table in zip(states, tables):
        state_text = state.text[-3:-1]
        districts = [
            matched.group(0)
            for row in table.find_all("tr")[1:]
            if (matched := patt.search(row.find_all(["th", "td"])[2].text.strip()))
        ]
        dist[f"IN-{state_text}"] = {"districts": districts, "total": len(districts)}

    return dict(sorted(dist.items()))


async def get_response(session: ClientSession, url: str) -> str:
    """
    Get response from the given url using aiohttp session.

    Args:
        session (ClientSession): `aiohttp` session
        url (str): URL to get response from.

    Returns:
        (str): response text
    """
    try:
        async with session.get(url) as response:
            return await response.text("utf-8")

    except Exception as e:
        print(e)
        return ""


if __name__ == "__main__":

    async def main():
        async with aiohttp.ClientSession() as session:
            states = asyncio.create_task(get_states(session))
            districts = asyncio.create_task(get_districts(session))
            for task in asyncio.as_completed([states, districts]):
                result = await task
                print(json.dumps(result, indent=2))

    asyncio.run(main())
