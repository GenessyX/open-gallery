from abc import ABC, abstractmethod

from open_gallery.hashing.interface import HashedValue
from open_gallery.identity.entities import User, UserId
from open_gallery.shared.repository import Repository
from open_gallery.shared.types import SecretValue


class UserRepository(Repository[UserId, User], ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> User | None: ...

    @abstractmethod
    async def get_by_refresh_token(self, hashed_token: SecretValue[HashedValue]) -> User | None: ...
