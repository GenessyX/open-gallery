from dataclasses import dataclass
from enum import Enum
from typing import Any

from open_gallery.images.entities import ImageId


@dataclass(kw_only=True)
class CreatePublicationDto:
    title: str
    linked_image_ids: list[ImageId]
    preview_image_id: ImageId
    document: Any


class ReactionType(str, Enum):
    LIKE = "like"
    UNLIKE = "unlike"
