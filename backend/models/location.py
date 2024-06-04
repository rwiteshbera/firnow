from pydantic import BaseModel


class State(BaseModel):
    name: str
    code: str
    country: str


class DistrictList(BaseModel):
    districts: list[str]
    total: int
