from pydantic import BaseModel, HttpUrl


class ErrorMessage(BaseModel):
    message: str


class ErrorMessageWithRedirect(ErrorMessage):
    redirect: HttpUrl


class ErrorMessageWithAction(ErrorMessage):
    action: HttpUrl


class RequestError(BaseModel):
    detail: ErrorMessage


class RequestErrorWithRedirect(BaseModel):
    detail: ErrorMessageWithRedirect


class RequestErrorWithAction(BaseModel):
    detail: ErrorMessageWithAction


class PoliceStationNotFound(Exception):
    pass
