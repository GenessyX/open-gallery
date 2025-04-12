from sqlalchemy import Boolean, String, Table, func, text
from sqlalchemy.orm import registry, relationship

from open_gallery.identity.entities import RefreshToken, User, VerificationCode
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import UserForeignKey, UserPrimaryKeyType
from open_gallery.persistence.type_decorators.datetime import UTCDateTime
from open_gallery.persistence.type_decorators.identity import UserRoleTypeImpl
from open_gallery.persistence.type_decorators.shared_types import SecretValueTypeImpl

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UserPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    *datetime_columns(),
    Column("email", String),
    Column("password", SecretValueTypeImpl),
    Column("role", UserRoleTypeImpl),
    Column("verified", Boolean, server_default=text("false")),
)

refresh_tokens = Table(
    "refresh_tokens",
    mapper_registry.metadata,
    Column("user_id", UserPrimaryKeyType, UserForeignKey(), primary_key=True),
    Column("token_hash", SecretValueTypeImpl, primary_key=True),
    Column("created_at", UTCDateTime, server_default=func.now()),
)

verification_codes = Table(
    "verification_codes",
    mapper_registry.metadata,
    Column("user_id", UserPrimaryKeyType, UserForeignKey(), primary_key=True),
    Column("code", String, primary_key=True),
    Column("created_at", UTCDateTime, server_default=func.now()),
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        RefreshToken,
        refresh_tokens,
    )

    mapper_registry.map_imperatively(
        VerificationCode,
        verification_codes,
    )

    mapper_registry.map_imperatively(
        User,
        users,
        properties={
            "refresh_tokens": relationship(
                RefreshToken,
                uselist=True,
                lazy="noload",
                cascade="save-update, merge, delete, delete-orphan",
            ),
            "verification_codes": relationship(
                VerificationCode,
                uselist=True,
                lazy="noload",
                cascade="save-update, merge, delete, delete-orphan",
            ),
        },
    )
