from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

from open_gallery.shared.entity import Entity, EntityId, SubEntity
from open_gallery.shared.types import Email, SecretValue

UserId = NewType("UserId", EntityId)


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass(kw_only=True)
class RefreshToken(SubEntity):
    token_hash: SecretValue[str]


@dataclass(kw_only=True)
class User(Entity):
    id: UserId = field(default_factory=lambda: UserId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    email: Email
    password: SecretValue[str]
    role: UserRole
    refresh_tokens: list[RefreshToken] = field(default_factory=list)
    verified: bool = False
