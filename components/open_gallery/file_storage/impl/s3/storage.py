from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, BinaryIO, override

from aiobotocore.session import get_session

from open_gallery.file_storage.impl.s3.settings import S3Settings
from open_gallery.file_storage.interface import ETag, FileStorage

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class S3FileStorage(FileStorage):
    def __init__(self, settings: S3Settings) -> None:
        self._session = get_session()
        self._settings = settings

    @property
    @asynccontextmanager
    async def _s3(self) -> AsyncIterator["S3Client"]:
        async with self._session.create_client(
            service_name="s3",
            region_name=self._settings.region,
            aws_access_key_id=self._settings.access_key.get_secret_value(),
            aws_secret_access_key=self._settings.secret_key.get_secret_value(),
            endpoint_url=self._settings.endpoint,
        ) as s3:
            yield s3

    @override
    async def upload(self, path: str, file: BinaryIO, mime_type: str) -> ETag:
        async with self._s3 as s3:
            response = await s3.put_object(
                Bucket=self._settings.bucket,
                Key=path,
                Body=file,
                ContentType=mime_type,
                ACL="public-read",
            )

        return response["ETag"]

    @override
    async def get(self, path: str) -> BinaryIO:
        async with self._s3 as s3:
            response = await s3.get_object(
                Bucket=self._settings.bucket,
                Key=path,
            )
        return response["Body"]
