from typing import Annotated

from fastapi import Body, Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from dependencies.auth import get_id_from_token
from models.auth import AccessToken
from models.errors import RequestErrorWithRedirect
from routes import police_station
from session import init
from utils.token import get_access_token_obj

auth_service = FastAPI(lifespan=init)

auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "https://api.firnow.duckdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_service.include_router(police_station.router)


@auth_service.get(
    "/refresh",
    responses={
        status.HTTP_200_OK: {
            "model": AccessToken,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": RequestErrorWithRedirect,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": RequestErrorWithRedirect,
        },
    },
    tags=["General Authentication Endpoints"],
    summary="Refresh access token",
)
async def refresh_token(
    response: Response, id: Annotated[int, Depends(get_id_from_token)]
):
    """
    This endpoint is used to refresh the access token.
    It requires `refresh_token` cookie to be set.
    """
    access_token_obj = await get_access_token_obj(id, response)
    return access_token_obj


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.auth:auth_service", port=8001)
