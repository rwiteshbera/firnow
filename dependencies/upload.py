from fastapi import HTTPException, Request, status
from starlette.requests import ClientDisconnect
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.validators import MaxSizeValidator, ValidationError

from models.errors import InvalidFileException, MaxBodySizeException
from models.upload_file import TemporaryUploadFile


async def get_file(request: Request) -> TemporaryUploadFile:
    try:
        size_validator = MaxSizeValidator(max_size=5 * 1024 * 1024)
        file = TemporaryUploadFile(validator=size_validator)
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", file)

        async for chunk in request.stream():
            parser.data_received(chunk)

        if file.content_type != "application/pdf":
            raise InvalidFileException

        return file

    except ClientDisconnect:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Client disconnected while uploading the file",
            },
        )

    except (MaxBodySizeException, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "message": "Maximum file size limit (5 MB) exceeded",
            },
        )

    except InvalidFileException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Only PDF files are allowed.",
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "There was an error uploading the file",
            },
        )


def check_size(request: Request) -> bool:
    if "content-length" not in request.headers:
        raise HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail={
                "message": "Content-Length header not found",
            },
        )

    content_length = int(request.headers["content-length"])
    if content_length > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "message": "Maximum file size limit (5 MB) exceeded",
            },
        )

    return True


def check_type(request: Request) -> bool:
    if "content-type" not in request.headers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Content-Type header not found",
            },
        )

    content_type = request.headers["content-type"]
    print(content_type)
    if content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Only PDF files are allowed.",
            },
        )

    return True
