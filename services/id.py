import time
from datetime import datetime

from fastapi import FastAPI, HTTPException

from models.errors import RequestError
from models.auth import Snowflake
from settings import config

id_service = FastAPI()
creation_date_string: str = config["APP_CREATION_DATE"] or "01 Jan 2023"
creation_date: datetime = datetime.strptime(creation_date_string, "%d %b %Y")
previous_offset: int = 0
node_id: int = int(config["NODE_ID"] or 0)
sequence_num: int = 0


@id_service.get(
    "/",
    responses={500: {"model": RequestError, "description": "Time exceeded"}},
)
def get_id() -> Snowflake:
    global previous_offset, node_id, sequence_num
    offset: int = round(time.time() - creation_date.timestamp())

    if (offset.bit_length()) > 41:
        raise HTTPException(status_code=500, detail="Time exceeded")

    sequence_bits: int = sequence_num.bit_length()
    sequence_num = (
        sequence_num + 1 if offset == previous_offset and sequence_bits <= 12 else 0
    )
    previous_offset = offset
    id_str = f"0b0{offset:041b}{node_id:010b}{sequence_num:012b}"
    return Snowflake(snowflake=int(id_str, 2))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.id:id_service", port=8001)
