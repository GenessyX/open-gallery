import datetime
from dataclasses import dataclass, field

from open_gallery.jwt.impl import Algorithm
from open_gallery.shared.types import SecretValue


@dataclass(kw_only=True)
class JWTSettings:
    secret: SecretValue[str] = field(default_factory=lambda: SecretValue("secret"))
    algorithm: Algorithm = "HS256"


@dataclass(kw_only=True)
class TokensSettings:
    access_token_ttl: datetime.timedelta = datetime.timedelta(days=7)
    refresh_token_ttl: datetime.timedelta = datetime.timedelta(days=30)


@dataclass(kw_only=True)
class IdentitySettings:
    tokens: TokensSettings = field(default_factory=TokensSettings)
    jwt: JWTSettings = field(default_factory=JWTSettings)
