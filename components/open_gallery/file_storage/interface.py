from abc import ABC, abstractmethod
from typing import BinaryIO

type ETag = str


class FileStorage(ABC):
    @abstractmethod
    async def upload(self, path: str, file: BinaryIO, mime_type: str) -> ETag: ...

    @abstractmethod
    async def get(self, path: str) -> BinaryIO: ...
