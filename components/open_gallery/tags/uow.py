from abc import ABC

from open_gallery.shared.uow import UnitOfWork
from open_gallery.tags.repository import TagRepository


class TagsUnitOfWork(UnitOfWork, ABC):
    tags: TagRepository
