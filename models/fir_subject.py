from pydantic import BaseModel


class FirSubject(BaseModel):
    id: int
    name: str
