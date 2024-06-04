import json
import logging
import random
import string
from calendar import c
from contextlib import asynccontextmanager
from re import A
from typing import Annotated, AsyncGenerator, Optional

import aiohttp
import uvicorn
from click import File
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from tortoise.exceptions import DoesNotExist
from typing_extensions import TypedDict

from config import Mode, get_log_config, settings
from databases.firestore import db
from databases.postgres import PostgresSession
from databases.web3 import w3
from dependencies.upload import get_file
from models.errors import RequestError
from models.fir_subject import FirSubject
from models.police_station import PoliceStationSearched_Pydantic
from models.tables import PoliceStation
from models.upload_file import TemporaryUploadFile
from session import SingletonSession


@asynccontextmanager
async def init(app: FastAPI):
    await PostgresSession.init()
    yield
    await PostgresSession.close()


general_service = FastAPI(lifespan=init)

logger = logging.getLogger("uvicorn.error")
logger.log(logging.INFO, "Starting general service")

general_service.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://localhost:3000",
        "https://api.firnow.duckdns.org",
        "http://api.firnow.duckdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@general_service.get(
    "/police-stations",
    summary="Get all registered police stations",
    response_model=list[PoliceStationSearched_Pydantic],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": RequestError,
            "description": "Police stations Not Found",
        },
    },
    tags=["General Endpoints"],
)
async def get_police_station(
    state: Optional[str] = None, district: Optional[str] = None
):
    """
    Get all police stations registered in the system. If no query parameters are provided,
    all police stations will be returned. If query parameters are provided, only police stations
    matching the query parameters will be returned.
    """
    police_stations = PoliceStation.all().filter(verified=True)

    if state:
        police_stations = police_stations.filter(state=state)
    if district:
        police_stations = police_stations.filter(district=district)

    police_stations = police_stations.order_by("state", "district")
    result = await PoliceStationSearched_Pydantic.from_queryset(police_stations)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Could not find any police stations",
            },
        )

    return result


@general_service.get(
    "/police-stations/{id}",
    summary="Get a police station by id",
    response_model=PoliceStationSearched_Pydantic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": RequestError,
            "description": "Police station Not Found",
        },
    },
    tags=["General Endpoints"],
)
async def get_police_station_by_id(id: int):
    """
    Get a police station by `id`. The `id` is unique integer helped to identify a police station.
    The `id` of police station can be obtained from `/police-stations` endpoint.
    """
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


@general_service.post(
    "/upload",
    responses={
        status.HTTP_200_OK: {
            "model": TypedDict("UploadResponse", {"cid": str}),
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": RequestError,
            "description": "Client Disconnected",
        },
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": RequestError,
            "description": "Maximum file size exceeded",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": RequestError,
            "description": "Invalid File Format",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": RequestError,
            "description": "Internal Server Error",
        },
    },
    tags=["General Endpoints"],
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
    """
    The FIR file must be in a PDF format and the content should be sent as a `multipart/form-data`.
    The maximum file size allowed is 5 MB.
    """
    session = SingletonSession.get_session()
    data = aiohttp.FormData()
    data.add_field("file", temp_file.file.read())
    data.add_field("pinataMetadata", json.dumps({"name": temp_file.filename}))
    data.add_field("pinataOptions", json.dumps({"cidVersion": 1}))
    async with session.post(
        f"https://api.pinata.cloud/pinning/pinFileToIPFS",
        data=data,
        headers={"Authorization": f"Bearer {settings.PINATA_JWT}"},
    ) as resp:
        result = await resp.json()

    temp_file.close()
    return {"cid": result["IpfsHash"]}


async def get_fir_file(
    cid: str, session: aiohttp.ClientSession
) -> AsyncGenerator[bytes, None]:
    async with session.get(f"{settings.PINATA_GATEWAY}ipfs/{cid}") as resp:
        async for data, _ in resp.content.iter_chunks():
            yield data


def generate_file_name() -> str:
    choices = string.ascii_letters + string.digits
    return f"FIR_{''.join(random.choices(choices, k=10))}.pdf"


@general_service.get(
    "/view/{cid}",
    tags=["General Endpoints"],
    responses={
        status.HTTP_200_OK: {
            "description": "View FIR file",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": RequestError,
            "description": "File Not Found",
        },
    },
)
async def view_file(cid: str):
    session = SingletonSession.get_session()
    return StreamingResponse(
        get_fir_file(cid, session),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={generate_file_name()}"},
    )


@general_service.get(
    "/fir-subjects",
    response_model=list[FirSubject],
    tags=["General Endpoints"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": RequestError,
            "description": "Subjects Not Found",
        },
    },
)
async def get_fir_subjects():
    """
    Get all FIR subjects
    """
    subjects: list[FirSubject] = [
        subject.to_dict()
        async for subject in db.collection("subjects").stream()  # type: ignore
    ]

    if not subjects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No FIR subjects found.",
            },
        )

    return subjects


if __name__ == "__main__":
    uvicorn.run(
        "services.general:general_service",
        port=8001,
        reload=True if settings.MODE == Mode.DEV else False,
        log_config=get_log_config("general_service"),
        workers=settings.UVICORN_WORKERS,
        access_log=settings.ACCESS_LOG,
    )
