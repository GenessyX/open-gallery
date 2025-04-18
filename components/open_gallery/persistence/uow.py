from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.identity.repository import UserRepository
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.images.repository import ImageRepository
from open_gallery.images.uow import ImagesUnitOfWork
from open_gallery.publications.repository import PublicationRepository
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.uow import UnitOfWork
from open_gallery.tags.repository import TagRepository
from open_gallery.tags.uow import TagsUnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def begin(self) -> None:
        if not self._session.sync_session.in_transaction():
            await self._session.begin()

    @override
    async def commit(self) -> None:
        await self._session.commit()

    @override
    async def rollback(self) -> None:
        await self._session.rollback()

    @override
    async def close(self) -> None:
        await self._session.close()


class SQLAlchemyIdentityUnitOfWork(SQLAlchemyUnitOfWork, IdentityUnitOfWork):
    def __init__(self, session: AsyncSession, user_repository: UserRepository) -> None:
        super().__init__(session)
        self.users = user_repository


class SQLAlchemyImagesUnitOfWork(SQLAlchemyUnitOfWork, ImagesUnitOfWork):
    def __init__(self, session: AsyncSession, image_repository: ImageRepository) -> None:
        super().__init__(session)
        self.images = image_repository


class SQLAlchemyPublicationsUnitOfWork(SQLAlchemyUnitOfWork, PublicationsUnitOfWork):
    def __init__(
        self,
        session: AsyncSession,
        publication_repository: PublicationRepository,
        image_repository: ImageRepository,
        tag_repository: TagRepository,
    ) -> None:
        super().__init__(session)
        self.publications = publication_repository
        self.images = image_repository
        self.tags = tag_repository


class SQLAlchemyTagsUnitOfWork(SQLAlchemyUnitOfWork, TagsUnitOfWork):
    def __init__(self, session: AsyncSession, tag_repository: TagRepository) -> None:
        super().__init__(session)
        self.tags = tag_repository
