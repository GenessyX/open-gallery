from sqlalchemy import Table, func
from sqlalchemy.orm import registry, relationship

from open_gallery.identity.entities import User
from open_gallery.notifications.entities import Notification
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import (
    NotificationPrimaryKeyType,
    PublicationForeignKey,
    PublicationPrimaryKeyType,
    UserForeignKey,
    UserPrimaryKeyType,
)
from open_gallery.persistence.tables.users import users
from open_gallery.persistence.type_decorators.notifications import NotificationSubjectTypeImpl
from open_gallery.publications.entities import Publication

notifications = Table(
    "notifications",
    mapper_registry.metadata,
    Column("id", NotificationPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey()),
    Column("actor_id", UserPrimaryKeyType, UserForeignKey()),
    Column("user_id", UserPrimaryKeyType, UserForeignKey()),
    Column("subject", NotificationSubjectTypeImpl),
    *datetime_columns(),
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        Notification,
        notifications,
        properties={
            "publication": relationship(
                Publication,
                uselist=False,
                lazy="joined",
            ),
            "actor": relationship(
                User,
                uselist=False,
                lazy="joined",
                primaryjoin=notifications.c.actor_id == users.c.id,
            ),
        },
    )
