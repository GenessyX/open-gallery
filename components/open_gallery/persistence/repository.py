from typing import override

from sqlalchemy import Table, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from open_gallery.persistence.exceptions import InvalidQueryError
from open_gallery.shared.entity import EntityIdT, EntityT
from open_gallery.shared.repository import Repository


class SQLAlchemyRepository(Repository[EntityIdT, EntityT]):
    def __init__(self, session: AsyncSession, table: Table, entity: type[EntityT]) -> None:
        self._table = table
        self._entity = entity
        self._session = session

    @override
    async def get(self, entity_id: EntityIdT) -> EntityT | None:
        stmt = select(self._entity).where(self._table.c.id == entity_id)
        result = await self._session.execute(stmt)
        return result.scalar()

    @override
    async def get_list(self, limit: int, offset: int) -> list[EntityT]:
        stmt = select(self._entity).order_by(self._table.c.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @override
    async def search(self, field: str, value: str) -> list[EntityT]:
        if not hasattr(self._entity, field):
            raise InvalidQueryError
        stmt = select(self._entity).where(getattr(self._table.c, field).ilike(f"%{value}%"))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    @override
    async def delete(self, entity_id: EntityIdT) -> None:
        stmt = delete(self._table).where(self._table.c.id == entity_id)
        await self._session.execute(stmt)

    @override
    async def save(self, entity: EntityT) -> EntityT:
        self._session.add(entity)
        return entity

    @override
    async def get_many(self, entity_ids: list[EntityIdT]) -> list[EntityT]:
        stmt = select(self._entity).where(self._table.c.id.in_(entity_ids))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
