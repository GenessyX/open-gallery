import mimetypes
from typing import BinaryIO, override

from open_gallery.file_storage.interface import FileStorage
from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.images.settings import ImagesSettings
from open_gallery.images.uow import ImagesUnitOfWork
from open_gallery.shared.use_case import Usecase


class UploadImageUsecase(Usecase):
    def __init__(
        self,
        uow: ImagesUnitOfWork,
        file_storage: FileStorage,
        images_settings: ImagesSettings,
    ) -> None:
        self._uow = uow
        self._file_storage = file_storage
        self._settings = images_settings

    @override
    async def __call__(self, actor: User, file: BinaryIO, mime_type: str) -> Image:
        async with self._uow as uow:
            image = Image.create(
                base_path=self._settings.base_path,
                uploaded_by=actor,
                file_extension=mimetypes.guess_extension(mime_type),
            )
            await self._file_storage.upload(
                path=image.path,
                file=file,
                mime_type=mime_type,
            )
            await uow.images.save(image)
        return image
