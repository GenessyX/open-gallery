from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.tags import tags
from open_gallery.tags.entities import Tag, TagId
from open_gallery.tags.repository import TagRepository


class SQLAlchemyTagRepository(SQLAlchemyRepository[TagId, Tag], TagRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, tags, Tag)
