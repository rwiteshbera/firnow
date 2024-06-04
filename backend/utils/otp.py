import random

from aiohttp import ClientSession
from pydantic import HttpUrl

from models.auth import SentOtpResponse
from session import SingletonSession


def generate_otp(n: int) -> str:
    otp = []
    for _ in range(n):
        otp.append(str(random.randint(0, 9)))
    return "".join(otp)


async def send_otp(url: HttpUrl, token: str) -> SentOtpResponse:
    session: ClientSession = SingletonSession.get_session()
    print(str(url))

    async with session.get(
        str(url),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    ) as resp:
        result = await resp.json()
        print(result)

    return SentOtpResponse(**result)
