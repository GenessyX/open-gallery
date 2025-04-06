from abc import ABC

from open_gallery.images.repository import ImageRepository
from open_gallery.publications.repository import PublicationRepository
from open_gallery.shared.uow import UnitOfWork


class PublicationsUnitOfWork(UnitOfWork, ABC):
    publications: PublicationRepository
    images: ImageRepository
