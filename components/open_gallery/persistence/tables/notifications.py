from sqlalchemy import UUID, Table, func
from sqlalchemy.orm import foreign, registry, relationship, remote

from open_gallery.identity.entities import User
from open_gallery.notifications.entities import CommentNotification, LikeNotification, Notification, NotificationType
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import (
    NotificationPrimaryKeyType,
    PublicationForeignKey,
    PublicationPrimaryKeyType,
    UserForeignKey,
    UserPrimaryKeyType,
)
from open_gallery.persistence.tables.users import users
from open_gallery.persistence.type_decorators.notifications import NotificationTypeTypeImpl
from open_gallery.publications.entities import Comment, Publication

notifications = Table(
    "notifications",
    mapper_registry.metadata,
    Column("id", NotificationPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey()),
    Column("actor_id", UserPrimaryKeyType, UserForeignKey()),
    Column("user_id", UserPrimaryKeyType, UserForeignKey()),
    Column("type", NotificationTypeTypeImpl),
    Column("related_object_id", UUID, nullable=True),
    *datetime_columns(),
)


def bind_mappers(mapper_registry: registry) -> None:
    from open_gallery.persistence.tables.publications import publication_comments

    mapper_registry.map_imperatively(
        Notification,
        notifications,
        polymorphic_on=notifications.c.type,
        polymorphic_identity="base",
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

    mapper_registry.map_imperatively(
        CommentNotification,
        notifications,
        inherits=Notification,
        polymorphic_identity=NotificationType.COMMENT,
        properties={
            "comment": relationship(
                Comment,
                uselist=False,
                lazy="joined",
                primaryjoin=foreign(notifications.c.related_object_id) == remote(publication_comments.c.id),
            ),
        },
    )

    mapper_registry.map_imperatively(
        LikeNotification,
        notifications,
        inherits=Notification,
        polymorphic_identity=NotificationType.LIKE,
        properties={},
    )
