import datetime
from typing import override

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, defer, selectinload

from open_gallery.identity.entities import UserId
from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.publications import (
    publication_comments,
    publication_likes,
    publication_views,
    publications,
)
from open_gallery.publications.entities import Comment, CommentId, Like, Publication, PublicationId, View
from open_gallery.publications.repository import PublicationRepository


class SQLAlchemyPublicationRepository(SQLAlchemyRepository[PublicationId, Publication], PublicationRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, publications, Publication)

    @override
    async def get_detail(self, publication_id: PublicationId) -> Publication | None:
        stmt = (select(Publication).where(publications.c.id == publication_id)).options(
            selectinload(Publication.images),  # type: ignore[arg-type]
            selectinload(Publication.references),  # type: ignore[arg-type]
            selectinload(Publication.tags),  # type: ignore[arg-type]
        )

        result = await self._session.execute(stmt)
        return result.scalar()

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

    @override
    async def get_not_approved(self, limit: int, offset: int) -> list[Publication]:
        stmt = (
            select(Publication)
            .where(publications.c.approved_by_id.is_(None))
            .order_by(publications.c.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @override
    async def get_with_views(self, publication_id: PublicationId, user_id: UserId) -> Publication | None:
        stmt = (
            select(Publication)
            .join(
                View,
                onclause=and_(
                    publications.c.id == publication_views.c.publication_id,
                    publication_views.c.user_id == user_id,
                ),
                isouter=True,
            )
            .where(publications.c.id == publication_id)
        ).options(
            contains_eager(Publication.views),  # type: ignore[arg-type]
            selectinload(Publication.images),  # type: ignore[arg-type]
            selectinload(Publication.references),  # type: ignore[arg-type]
            selectinload(Publication.tags),  # type: ignore[arg-type]
        )

        result = await self._session.execute(stmt)
        return result.scalar()

    @override
    async def get_with_likes(self, publication_id: PublicationId, user_id: UserId) -> Publication | None:
        stmt = (
            select(Publication)
            .join(
                Like,
                onclause=and_(
                    publications.c.id == publication_likes.c.publication_id,
                    publication_likes.c.user_id == user_id,
                ),
                isouter=True,
            )
            .where(publications.c.id == publication_id)
        ).options(
            contains_eager(Publication.likes),  # type: ignore[arg-type]
        )

        result = await self._session.execute(stmt)
        return result.scalar()

    @override
    async def get_comments(self, publication_id: PublicationId, limit: int, offset: int) -> list[Comment]:
        stmt = (
            select(Comment)
            .where(
                and_(
                    publication_comments.c.publication_id == publication_id,
                    publication_comments.c.parent_id.is_(None),
                ),
            )
            .order_by(publication_comments.c.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @override
    async def get_with_comment(self, publication_id: PublicationId, comment_id: CommentId) -> Publication | None:
        stmt = (
            select(Publication)
            .join(
                Comment,
                onclause=and_(
                    publications.c.id == publication_comments.c.publication_id,
                    publication_comments.c.id == comment_id,
                ),
            )
            .where(publications.c.id == publication_id)
            .options(
                contains_eager(Publication.comments),  # type: ignore[arg-type]
                defer(Publication.comments_count),  # type: ignore[arg-type]
                defer(Publication.likes_count),  # type: ignore[arg-type]
                defer(Publication.views_count),  # type: ignore[arg-type]
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar()

    @override
    async def get_popular(self, limit: int, since: datetime.timedelta) -> list[Publication]:
        created_since = datetime.datetime.now(datetime.UTC) - since
        stmt = (
            select(Publication)
            .where(publications.c.approved_by_id.is_not(None))
            .where(publications.c.created_at >= created_since)
            .order_by(Publication.views_count.desc())  # type: ignore[attr-defined]
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
