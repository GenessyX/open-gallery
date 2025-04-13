from abc import ABC

from open_gallery.images.repository import ImageRepository
from open_gallery.publications.repository import PublicationRepository
from open_gallery.shared.uow import UnitOfWork
from open_gallery.tags.repository import TagRepository


class PublicationsUnitOfWork(UnitOfWork, ABC):
    publications: PublicationRepository
    images: ImageRepository
    tags: TagRepository
