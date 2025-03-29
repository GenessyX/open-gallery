from abc import ABC
from dataclasses import dataclass

from open_gallery.identity.repository import UserRepository
from open_gallery.shared.uow import UnitOfWork


@dataclass(kw_only=True)
class IdentityUnitOfWork(UnitOfWork, ABC):
    users: UserRepository
