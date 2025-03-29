from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.shared.uow import UnitOfWork


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
