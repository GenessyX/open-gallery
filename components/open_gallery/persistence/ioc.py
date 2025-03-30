from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.identity.entities import User, UserId
from open_gallery.identity.repository import UserRepository
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.persistence.database import Database
from open_gallery.persistence.repository import SQLAlchemyRepository
from open_gallery.persistence.tables.users import users
from open_gallery.persistence.uow import SQLAlchemyIdentityUnitOfWork


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

    @provide
    def users(self, session: AsyncSession) -> UserRepository:
        return SQLAlchemyRepository[UserId, User](session=session, table=users, entity=User)


class UnitsOfWorkProvider(Provider):
    scope = Scope.REQUEST

    identity = provide(SQLAlchemyIdentityUnitOfWork, provides=IdentityUnitOfWork)
