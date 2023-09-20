from pydantic import BaseModel


class RequestError(BaseModel):
    detail: str
