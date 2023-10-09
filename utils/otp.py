import random

from aiohttp import ClientSession
from pydantic import HttpUrl

from models.auth import OTPSentResponse
from session import SingletonSession


def generate_otp(n: int) -> str:
    otp = []
    for _ in range(n):
        otp.append(str(random.randint(0, 9)))
    return "".join(otp)


async def send_otp(url: str, token: str) -> OTPSentResponse:
    session: ClientSession = SingletonSession.get_session()

    async with session.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    ) as resp:
        result = await resp.json()
        print(result)

    return OTPSentResponse(**result)
