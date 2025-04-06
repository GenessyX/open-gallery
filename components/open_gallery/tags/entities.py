from dataclasses import dataclass, field
from typing import NewType

from open_gallery.shared.entity import Entity, EntityId

TagId = NewType("TagId", EntityId)


@dataclass(kw_only=True)
class Tag(Entity):
    id: TagId = field(default_factory=lambda: TagId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    title: str
    children: list["Tag"] = field(default_factory=list)
