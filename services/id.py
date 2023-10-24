import time
from csv import list_dialects
from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from config import settings
from models.auth import Snowflake
from models.errors import RequestError
from session import init

id_service = FastAPI(lifespan=init)


creation_date: datetime = settings.APP_CREATION_DATE
previous_offset: int = 0
node_id: int = settings.NODE_ID
sequence_num: int = 0


@id_service.get(
    "/",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": RequestError,
        }
    },
)
def get_id() -> Snowflake:
    global previous_offset, node_id, sequence_num
    offset: int = round(time.time() - creation_date.timestamp())

    if (offset.bit_length()) > 41:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Time exceeded"},
        )

    sequence_bits: int = sequence_num.bit_length()
    sequence_num = (
        sequence_num + 1 if offset == previous_offset and sequence_bits <= 12 else 0
    )
    previous_offset = offset
    id_str = f"0b0{offset:041b}{node_id:010b}{sequence_num:012b}"
    return Snowflake(snowflake=int(id_str, 2))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.id:id_service", port=8002)
