from sqlalchemy.orm import registry

from open_gallery.persistence.tables.images import bind_mappers as bind_image_mappers
from open_gallery.persistence.tables.users import bind_mappers as bind_user_mappers


def bind_mappers(mapper_registry: registry) -> None:
    bind_user_mappers(mapper_registry)
    bind_image_mappers(mapper_registry)
