from typing import Optional, cast

from fastapi import FastAPI, HTTPException, status

from databases.firestore import db
from models.errors import RequestError
from models.location import DistrictList, State

location_service = FastAPI()


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
