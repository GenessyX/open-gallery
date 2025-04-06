from dataclasses import dataclass, field
from typing import Any, NewType

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.shared.entity import Entity, EntityId, SubEntity
from open_gallery.tags.entities import Tag

PublicationId = NewType("PublicationId", EntityId)
CommentId = NewType("CommentId", EntityId)


@dataclass(kw_only=True)
class Comment(Entity):
    id: CommentId = field(default_factory=lambda: CommentId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    text: str
    author: User


@dataclass(kw_only=True)
class Like(SubEntity):
    user: User


@dataclass(kw_only=True)
class View(SubEntity):
    user: User


@dataclass(kw_only=True)
class Publication(Entity):
    id: PublicationId = field(default_factory=lambda: PublicationId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    title: str
    images: list[Image] = field(default_factory=list)
    preview: Image
    created_by: User
    document: Any
    approved_by: User | None
    comments: list[Comment] = field(default_factory=list)
    likes: list[Like] = field(default_factory=list)
    views: list[View] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)

    def approve(self, actor: User) -> None:
        self.approved_by = actor
