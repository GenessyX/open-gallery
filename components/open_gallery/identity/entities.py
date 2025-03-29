from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

from open_gallery.shared.entity import Entity, EntityId
from open_gallery.shared.types import Email, SecretValue

UserId = NewType("UserId", EntityId)


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass(kw_only=True)
class User(Entity):
    id: UserId = field(default_factory=lambda: UserId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    email: Email
    password: SecretValue[str]
    role: UserRole
