from abc import ABC, abstractmethod

from open_gallery.hashing.interface import HashedValue
from open_gallery.identity.entities import User, UserId
from open_gallery.notifications.entities import GenericNotification
from open_gallery.shared.repository import Repository
from open_gallery.shared.types import Email, SecretValue


class UserRepository(Repository[UserId, User], ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> list[User]: ...

    @abstractmethod
    async def get_verified_by_email(self, email: Email) -> User | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> User | None: ...

    @abstractmethod
    async def get_by_refresh_token(self, hashed_token: SecretValue[HashedValue]) -> User | None: ...

    @abstractmethod
    async def get_notifications(self, user_id: UserId, limit: int, offset: int) -> list[GenericNotification]: ...
