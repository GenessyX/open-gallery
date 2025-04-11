from dataclasses import dataclass, field
from typing import Any, NewType

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.publications.exceptions import InvalidLikeError, InvalidUnlikeError
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

    comments: list[Comment] = field(default_factory=list, repr=False)
    comments_count: int = field(default=0)

    likes: list[Like] = field(default_factory=list, repr=False)
    likes_count: int = field(default=0)

    views: list[View] = field(default_factory=list, repr=False)
    views_count: int = field(default=0)

    tags: list[Tag] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.views_count = len(self.views)

    def approve(self, actor: User) -> None:
        self.approved_by = actor

    def view(self, actor: User) -> None:
        self.views.append(View(user=actor))
        self.views_count += 1

    def get_like(self, actor: User) -> Like | None:
        return next((like for like in self.likes if like.user == actor), None)

    def like(self, actor: User) -> None:
        existing_like = self.get_like(actor)
        if existing_like:
            raise InvalidLikeError(self.id)

        self.likes.append(Like(user=actor))
        self.likes_count += 1

    def unlike(self, actor: User) -> None:
        existing_like = self.get_like(actor)
        if not existing_like:
            raise InvalidUnlikeError(self.id)

        self.likes.remove(existing_like)
        self.likes_count -= 1

    def add_comment(self, text: str, actor: User) -> Comment:
        comment = Comment(text=text, author=actor)
        self.comments.append(comment)
        self.comments_count += 1
        return comment
