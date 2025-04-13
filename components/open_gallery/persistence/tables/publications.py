from sqlalchemy import JSON, String, Table, func, inspect, select
from sqlalchemy.event import listen
from sqlalchemy.orm import QueryContext, column_property, registry, relationship

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import (
    ImageForeignKey,
    ImagePrimaryKeyType,
    PublicationCommentPrimaryKeyType,
    PublicationForeignKey,
    PublicationPrimaryKeyType,
    TagForeignKey,
    TagPrimaryKeyType,
    UserForeignKey,
    UserPrimaryKeyType,
)
from open_gallery.persistence.tables.users import users
from open_gallery.persistence.type_decorators.datetime import UTCDateTime
from open_gallery.publications.entities import Comment, Like, Publication, View
from open_gallery.tags.entities import Tag

publications = Table(
    "publications",
    mapper_registry.metadata,
    Column("id", PublicationPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    Column("title", String),
    Column("preview_id", ImagePrimaryKeyType, ImageForeignKey()),
    Column("created_by_id", UserPrimaryKeyType, UserForeignKey()),
    Column("approved_by_id", UserPrimaryKeyType, UserForeignKey(), nullable=True),
    Column("document", JSON),
    *datetime_columns(),
)

publication_images = Table(
    "publication_images",
    mapper_registry.metadata,
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey(), primary_key=True),
    Column("image_id", ImagePrimaryKeyType, ImageForeignKey(), primary_key=True),
)

publication_comments = Table(
    "publication_comments",
    mapper_registry.metadata,
    Column("id", PublicationCommentPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey()),
    Column("author_id", UserPrimaryKeyType, UserForeignKey()),
    Column("text", String),
    *datetime_columns(),
)

publication_likes = Table(
    "publication_likes",
    mapper_registry.metadata,
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey(), primary_key=True),
    Column("user_id", UserPrimaryKeyType, UserForeignKey(), primary_key=True),
    Column("created_at", UTCDateTime, server_default=func.now()),
)

publication_views = Table(
    "publication_views",
    mapper_registry.metadata,
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey(), primary_key=True),
    Column("user_id", UserPrimaryKeyType, UserForeignKey(), primary_key=True),
    Column("created_at", UTCDateTime, server_default=func.now()),
)

publication_tags = Table(
    "publication_tags",
    mapper_registry.metadata,
    Column("publication_id", PublicationPrimaryKeyType, PublicationForeignKey(), primary_key=True),
    Column("tag_id", TagPrimaryKeyType, TagForeignKey(), primary_key=True),
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        Comment,
        publication_comments,
        properties={
            "author": relationship(
                User,
                uselist=False,
                lazy="joined",
            ),
        },
    )

    mapper_registry.map_imperatively(
        Like,
        publication_likes,
        properties={
            "user": relationship(
                User,
                uselist=False,
                lazy="joined",
            ),
        },
    )

    mapper_registry.map_imperatively(
        View,
        publication_views,
        properties={
            "user": relationship(
                User,
                uselist=False,
                lazy="joined",
            ),
        },
    )

    mapper_registry.map_imperatively(
        Publication,
        publications,
        properties={
            "comments": relationship(
                Comment,
                uselist=True,
                lazy="noload",
                order_by=publication_comments.c.created_at.desc(),
                cascade="all, delete-orphan",
            ),
            "comments_count": column_property(
                select(func.count(publication_comments.c.author_id))
                .where(publication_comments.c.publication_id == publications.c.id)
                .correlate_except(publication_comments)
                .scalar_subquery(),
                expire_on_flush=False,
            ),
            "likes": relationship(
                Like,
                uselist=True,
                lazy="noload",
                order_by=publication_likes.c.created_at.desc(),
                cascade="all, delete-orphan",
            ),
            "likes_count": column_property(
                select(func.count(publication_likes.c.user_id))
                .where(publication_likes.c.publication_id == publications.c.id)
                .correlate_except(publication_likes)
                .scalar_subquery(),
                expire_on_flush=False,
            ),
            "views": relationship(
                View,
                uselist=True,
                lazy="noload",
                order_by=publication_views.c.created_at.desc(),
            ),
            "views_count": column_property(
                select(func.count(publication_views.c.user_id))
                .where(publication_views.c.publication_id == publications.c.id)
                .correlate_except(publication_views)
                .scalar_subquery(),
                expire_on_flush=False,
            ),
            "preview": relationship(
                Image,
                uselist=False,
                lazy="joined",
            ),
            "created_by": relationship(
                User,
                uselist=False,
                lazy="joined",
                primaryjoin=publications.c.created_by_id == users.c.id,
            ),
            "approved_by": relationship(
                User,
                uselist=False,
                lazy="joined",
                primaryjoin=publications.c.approved_by_id == users.c.id,
            ),
            "images": relationship(
                Image,
                uselist=True,
                lazy="noload",
                secondary=publication_images,
            ),
            "tags": relationship(
                Tag,
                uselist=True,
                lazy="selectin",
                secondary=publication_tags,
            ),
        },
    )

    def load_publication(target: Publication, _: QueryContext) -> None:
        ins = inspect(target)
        unloaded_attributes: set[str] = ins.unloaded  # type: ignore[union-attr]

        if "comments_count" in unloaded_attributes:
            target.comments_count = len(target.comments)
        if "likes_count" in unloaded_attributes:
            target.likes_count = len(target.likes)
        if "views_count" in unloaded_attributes:
            target.views_count = len(target.views)

    listen(Publication, "load", load_publication)
