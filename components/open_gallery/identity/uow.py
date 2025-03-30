from abc import ABC

from open_gallery.identity.repository import UserRepository
from open_gallery.shared.uow import UnitOfWork


class IdentityUnitOfWork(UnitOfWork, ABC):
    users: UserRepository
