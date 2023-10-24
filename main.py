import asyncio
from typing import Annotated, Optional

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.exceptions import DoesNotExist
from typing_extensions import TypedDict

from config import Mode, settings
from databases.web3 import w3
from dependencies.upload import get_file
from models.errors import RequestError
from models.police_station import PoliceStationSearched_Pydantic
from models.tables import PoliceStation
from models.upload_file import TemporaryUploadFile
from session import init

app = FastAPI(lifespan=init)

if settings.MODE == Mode.DEV:
    print("Running in development mode")
    from services.auth import auth_service
    from services.id import id_service
    from services.location import location_service

    app.mount("/auth", auth_service)
    app.mount("/id", id_service)
    app.mount("/location", location_service)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "https://api.firnow.duckdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/police-stations",
    summary="Get all registered police stations",
    response_model=list[PoliceStationSearched_Pydantic],
    tags=["Police Station Endpoints"],
)
async def get_police_station(
    state: Optional[str] = None, district: Optional[str] = None
):
    police_stations = PoliceStation.all().filter(verified=True)

    if state:
        police_stations = police_stations.filter(state=state)
    if district:
        police_stations = police_stations.filter(district=district)

    police_stations = police_stations.order_by("state", "district")
    return await PoliceStationSearched_Pydantic.from_queryset(police_stations)


@app.get(
    "/police-stations/{id}",
    summary="Get a police station by id",
    response_model=PoliceStationSearched_Pydantic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": RequestError,
        },
    },
    tags=["Police Station Endpoints"],
)
async def get_police_station_by_id(id: int):
    try:
        police_station = await PoliceStation.get(id=id)
        return await PoliceStationSearched_Pydantic.from_tortoise_orm(police_station)

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Police station not found with the given ID.",
            },
        )


@app.post(
    "/upload",
    responses={
        status.HTTP_200_OK: {
            "model": TypedDict("UploadResponse", {"cid": str}),
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": RequestError,
        },
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": RequestError,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": RequestError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": RequestError,
        },
    },
    tags=["File Uploading Endpoint"],
    openapi_extra={
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "file": {
                                "type": "string",
                                "format": "binary",
                            },
                        },
                    },
                },
            },
            "required": True,
        }
    },
)
async def upload_file(temp_file: Annotated[TemporaryUploadFile, Depends(get_file)]):
    fir_cid: str = await asyncio.to_thread(
        w3.post_upload, (temp_file.filename, temp_file.file)
    )
    temp_file.close()
    return {"cid": fir_cid}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8000, reload=True if settings.MODE == Mode.DEV else False
    )
