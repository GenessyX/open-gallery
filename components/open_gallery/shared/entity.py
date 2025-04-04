import datetime
from dataclasses import dataclass, field
from typing import Any, Self, TypeVar, override
from uuid import UUID

from uuid_extensions import uuid7str

from open_gallery.shared.sentinel import NO_ARG


class EntityId(UUID):
    @classmethod
    def generate(cls) -> Self:
        return cls(hex=uuid7str())


@dataclass(kw_only=True)
class Entity:
    id: EntityId = field(default_factory=EntityId.generate)
    created_at: datetime.datetime = field(default=NO_ARG)  # type: ignore[assignment]
    updated_at: datetime.datetime = field(default=NO_ARG)  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.created_at is NO_ARG:
            self.created_at = datetime.datetime.now(datetime.UTC)
            self.updated_at = self.created_at

    @override
    def __setattr__(self, name: str, value: Any, /) -> None:
        super().__setattr__(name, value)
        if name != "updated_at" and name in self.__dataclass_fields__:
            object.__setattr__(self, "updated_at", datetime.datetime.now(datetime.UTC))


@dataclass(kw_only=True)
class SubEntity:
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))


EntityIdT = TypeVar("EntityIdT", bound=EntityId)
EntityT = TypeVar("EntityT", bound=Entity)
