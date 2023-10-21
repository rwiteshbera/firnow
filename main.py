from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import DoesNotExist

from models.errors import RequestError
from models.police_station import PoliceStation_Pydantic
from models.tables import PoliceStation
from models.upload_file import TemporaryUploadFile
from services.auth import auth_service
from services.id import id_service
from services.location import location_service
from session import manage_session
from utils.dependencies import get_file

app = FastAPI(lifespan=manage_session, prefix="/main")


@app.get(
    "/police-stations",
    summary="Get all registered police stations",
    response_model=list[PoliceStation_Pydantic],
    tags=["Police Station Endpoints"],
)
async def get_police_station():
    police_stations = PoliceStation.all().order_by("state", "district")
    return await PoliceStation_Pydantic.from_queryset(police_stations)


@app.get(
    "/police-stations/{id}",
    summary="Get a police station by id",
    response_model=PoliceStation_Pydantic,
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
        return await PoliceStation_Pydantic.from_tortoise_orm(police_station)

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Police station not found with the given ID.",
            },
        )


@app.post("/file")
async def upload_file(file: Annotated[TemporaryUploadFile, Depends(get_file)]):
    filename = file.filename
    file.close()
    return {"filename": filename}


app.mount("/auth", auth_service)
app.mount("/id", id_service)
app.mount("/location", location_service)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
