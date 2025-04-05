from pathlib import Path
from typing import BinaryIO, override

from open_gallery.file_storage.interface import FileStorage
from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.images.uow import ImagesUnitOfWork
from open_gallery.shared.use_case import Usecase


class UploadImageUsecase(Usecase):
    def __init__(
        self,
        uow: ImagesUnitOfWork,
        file_storage: FileStorage,
    ) -> None:
        self._uow = uow
        self._file_storage = file_storage

    @override
    async def __call__(self, actor: User, file: BinaryIO) -> Image:
        async with self._uow as uow:
            image = Image.create(base_path=Path("attachments"), uploaded_by=actor)
            await self._file_storage.upload(path=image.path, file=file)
            await uow.images.save(image)
        return image
