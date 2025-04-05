from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.identity.repository import UserRepository
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.images.repository import ImageRepository
from open_gallery.images.uow import ImagesUnitOfWork
from open_gallery.persistence.database import Database
from open_gallery.persistence.repositories.images import SQLAlchemyImageRepository
from open_gallery.persistence.repositories.users import SQLAlchemyUserRepository
from open_gallery.persistence.uow import SQLAlchemyIdentityUnitOfWork, SQLAlchemyImagesUnitOfWork


class DatabaseProvider(Provider):
    scope = Scope.APP

    database = provide(Database)

    @provide(scope=Scope.REQUEST)
    async def session(self, database: Database) -> AsyncIterator[AsyncSession]:
        session = database.get_async_session()
        yield session
        await session.close()


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    users = provide(SQLAlchemyUserRepository, provides=UserRepository)
    images = provide(SQLAlchemyImageRepository, provides=ImageRepository)


class UnitsOfWorkProvider(Provider):
    scope = Scope.REQUEST

    identity = provide(SQLAlchemyIdentityUnitOfWork, provides=IdentityUnitOfWork)
    images = provide(SQLAlchemyImagesUnitOfWork, provides=ImagesUnitOfWork)
