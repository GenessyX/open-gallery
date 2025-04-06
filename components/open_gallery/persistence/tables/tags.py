from sqlalchemy import String, Table, func
from sqlalchemy.orm import registry, relationship

from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import (
    TagForeignKey,
    TagPrimaryKeyType,
)
from open_gallery.tags.entities import Tag

tags = Table(
    "tags",
    mapper_registry.metadata,
    Column("id", TagPrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    Column("title", String),
    Column("parent_id", TagPrimaryKeyType, TagForeignKey(), nullable=True),
    *datetime_columns(),
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        Tag,
        tags,
        properties={
            "children": relationship(
                Tag,
                uselist=True,
                lazy="selectin",
                primaryjoin=tags.c.id == tags.c.parent_id,
                remote_side=[tags.c.parent_id],
                join_depth=20,
            ),
        },
    )
