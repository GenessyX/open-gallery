from dataclasses import dataclass, field
from pathlib import Path
from typing import NewType

from open_gallery.identity.entities import User
from open_gallery.shared.entity import Entity, EntityId

ImageId = NewType("ImageId", EntityId)


@dataclass(kw_only=True)
class Image(Entity):
    id: ImageId = field(default_factory=lambda: ImageId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    path: str
    uploaded_by: User

    @classmethod
    def create(cls, base_path: Path, uploaded_by: User, file_extension: str | None) -> "Image":
        image_id = ImageId(EntityId.generate())
        file_name = f"{image_id}{file_extension}" if file_extension else str(image_id)
        return Image(
            id=image_id,
            path=str(base_path / file_name),
            uploaded_by=uploaded_by,
        )
