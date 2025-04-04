from dataclasses import dataclass

from open_gallery.identity.entities import UserRole
from open_gallery.jwt.interface import SerializedToken
from open_gallery.jwt.payload import JWTPayload


@dataclass(kw_only=True)
class TokensPair:
    access_token: SerializedToken
    refresh_token: SerializedToken


@dataclass(kw_only=True)
class AccessTokenPayload(JWTPayload):
    role: UserRole


@dataclass(kw_only=True)
class RefreshTokenPayload(JWTPayload): ...
