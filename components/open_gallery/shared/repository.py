from abc import ABC, abstractmethod
from typing import Generic

from open_gallery.shared.entity import EntityIdT, EntityT


class Repository(ABC, Generic[EntityIdT, EntityT]):
    @abstractmethod
    async def get(self, entity_id: EntityIdT) -> EntityT | None: ...

    @abstractmethod
    async def get_many(self, entity_ids: list[EntityIdT]) -> list[EntityT]: ...

    @abstractmethod
    async def get_list(self, limit: int, offset: int) -> list[EntityT]: ...

    @abstractmethod
    async def delete(self, entity_id: EntityIdT) -> None: ...

    @abstractmethod
    async def save(self, entity: EntityT) -> EntityT: ...
