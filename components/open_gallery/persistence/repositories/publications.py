from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.publications import publications
from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.publications.repository import PublicationRepository


class SQLAlchemyPublicationRepository(SQLAlchemyRepository[PublicationId, Publication], PublicationRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, publications, Publication)

    @override
    async def get_list(self, limit: int, offset: int) -> list[Publication]:
        stmt = (
            select(Publication)
            .where(publications.c.approved_by_id.is_not(None))
            .order_by(publications.c.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
