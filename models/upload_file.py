from tempfile import TemporaryFile
from typing import IO, Optional

from starlette.datastructures import Headers
from streaming_form_data.targets import BaseTarget


class TemporaryUploadFile(BaseTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename: Optional[str] = None
        self.content_type: Optional[str] = None
        self.file: IO[bytes] = TemporaryFile()

    def on_data_received(self, chunk: bytes):
        self.file.write(chunk)

    def on_finish(self):
        self.filename = self.multipart_filename
        self.content_type = self.multipart_content_type

    def read(self, size: int = -1) -> bytes:
        return self.file.read(size)

    def seek(self, offset: int, whence: int = 0) -> None:
        self.file.seek(offset, whence)

    def close(self) -> None:
        self.file.close()
