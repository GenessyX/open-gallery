import datetime
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class JWTPayload:
    sub: str
    iss: str = "api"
    exp: datetime.datetime | None = None
    iat: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
