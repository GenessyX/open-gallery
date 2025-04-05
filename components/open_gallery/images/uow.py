from abc import ABC

from open_gallery.images.repository import ImageRepository
from open_gallery.shared.uow import UnitOfWork


class ImagesUnitOfWork(UnitOfWork, ABC):
    images: ImageRepository
