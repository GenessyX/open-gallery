from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.images.entities import Image, ImageId
from open_gallery.images.repository import ImageRepository
from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.images import images


class SQLAlchemyImageRepository(SQLAlchemyRepository[ImageId, Image], ImageRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, images, Image)
