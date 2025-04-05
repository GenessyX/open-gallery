from dataclasses import dataclass, field

from open_gallery.shared.types import SecretValue


@dataclass(kw_only=True)
class S3Settings:
    region: str = "us-east-1"
    access_key: SecretValue[str] = field(default_factory=lambda: SecretValue("access_key"))
    secret_key: SecretValue[str] = field(default_factory=lambda: SecretValue("secret_key"))
    endpoint: str = "http://localhost:9000"
    bucket: str = "public"
