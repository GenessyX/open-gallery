from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.publications import publications
from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.publications.repository import PublicationRepository


class SQLAlchemyPublicationRepository(SQLAlchemyRepository[PublicationId, Publication], PublicationRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, publications, Publication)
