from dataclasses import dataclass

from open_gallery.identity.entities import UserRole
from open_gallery.jwt.interface import SerializedToken
from open_gallery.jwt.payload import JWTPayload
from open_gallery.shared.types import Email


@dataclass(kw_only=True)
class TokensPair:
    access_token: SerializedToken
    refresh_token: SerializedToken


@dataclass(kw_only=True)
class AccessTokenPayload(JWTPayload):
    role: UserRole
    email: Email


@dataclass(kw_only=True)
class RefreshTokenPayload(JWTPayload): ...
