import logging
from typing import Optional, cast

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from config import Mode, get_log_config, settings
from databases.firestore import db
from models.errors import RequestError
from models.location import DistrictList, State
from session import init

location_service = FastAPI(lifespan=init)

logger = logging.getLogger("uvicorn.error")
logger.log(logging.INFO, "Starting location service")

location_service.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "https://api.firnow.duckdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@location_service.get(
    "/states",
    tags=["Location"],
    summary="Get all states of the country",
)
async def get_states() -> list[State]:
    states: list[State] = [
        state.to_dict()
        async for state in db.collection("states").stream()  # type: ignore
    ]
    return states


@location_service.get(
    "/states/{state_code}",
    tags=["Location"],
    summary="Get the state by state code",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": RequestError,
        },
    },
)
async def get_state(state_code: str) -> State:
    state = await db.collection("states").document(state_code).get()
    st: Optional[State] = cast(State, state.to_dict())
    if st is None:
        raise HTTPException(status_code=400, detail={"message": "Invalid state code"})
    return st


@location_service.get(
    "/states/{state_code}/districts",
    tags=["Location"],
    summary="Get all districts of the state",
    responses={
        status.HTTP_200_OK: {
            "example": {"districts": ["district1", "district2"], "total": 2}
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": RequestError,
        },
    },
)
async def get_districts(state_code: str) -> DistrictList:
    district = await db.collection("districts").document(state_code).get()
    dist: Optional[DistrictList] = cast(DistrictList, district.to_dict())
    if dist is None:
        raise HTTPException(status_code=400, detail={"message": "Invalid state code"})
    return dist


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services.location:location_service",
        port=8003,
        reload=True if settings.MODE == Mode.DEV else False,
        log_config=get_log_config("location_service"),
        workers=settings.UVICORN_WORKERS,
        access_log=settings.ACCESS_LOG,
    )
