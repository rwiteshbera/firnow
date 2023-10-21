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


class MaxBodySizeException(Exception):
    def __init__(self, body_len: int):
        self.body_len = body_len
        super().__init__()


class InvalidFileException(Exception):
    pass
