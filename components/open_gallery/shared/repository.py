from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from open_gallery.shared.entity import Entity, EntityId

EntityT = TypeVar("EntityT", bound=Entity)
EntityIdT = TypeVar("EntityIdT", bound=EntityId)


class Repository(ABC, Generic[EntityIdT, EntityT]):
    @abstractmethod
    async def get(self, entity_id: EntityIdT) -> EntityT | None: ...

    @abstractmethod
    async def delete(self, entity_id: EntityIdT) -> None: ...

    @abstractmethod
    async def save(self, eneity: EntityT) -> EntityT: ...
