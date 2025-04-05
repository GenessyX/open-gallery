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
class VerificationCode(SubEntity):
    code: str


@dataclass(kw_only=True)
class User(Entity):
    id: UserId = field(default_factory=lambda: UserId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    email: Email
    password: SecretValue[str]
    role: UserRole
    refresh_tokens: list[RefreshToken] = field(default_factory=list)
    verification_codes: list[VerificationCode] = field(default_factory=list)
    verified: bool = False

    def add_refresh_token(self, token_hash: str) -> None:
        self.refresh_tokens.append(RefreshToken(token_hash=SecretValue(token_hash)))

    def add_verification_code(self, code: str) -> None:
        self.verification_codes.append(VerificationCode(code=code))

    def verify(self, code: str) -> bool:
        verification_code = self.get_code(code)
        if verification_code is None:
            return False
        self.verification_codes.remove(verification_code)
        self.verified = True
        return True

    def get_code(self, code: str) -> VerificationCode | None:
        return next(
            (verification_code for verification_code in self.verification_codes if verification_code.code == code),
            None,
        )
