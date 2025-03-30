from sqlalchemy import String, Table, func
from sqlalchemy.orm import registry

from open_gallery.identity.entities import User
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import UserPrimaryKeyType
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
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        User,
        users,
    )
