from sqlalchemy import String, Table, func
from sqlalchemy.orm import registry, relationship

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.persistence.tables.base import Column, datetime_columns, mapper_registry
from open_gallery.persistence.tables.keys import ImagePrimaryKeyType, UserForeignKey, UserPrimaryKeyType

images = Table(
    "images",
    mapper_registry.metadata,
    Column("id", ImagePrimaryKeyType, primary_key=True, server_default=func.gen_random_uuid()),
    *datetime_columns(),
    Column("path", String),
    Column("uploaded_by_id", UserPrimaryKeyType, UserForeignKey()),
)


def bind_mappers(mapper_registry: registry) -> None:
    mapper_registry.map_imperatively(
        Image,
        images,
        properties={
            "uploaded_by": relationship(
                User,
                uselist=False,
                lazy="joined",
            ),
        },
    )
