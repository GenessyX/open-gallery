from dataclasses import dataclass, field
from typing import Any, NewType

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.notifications.entities import CommentNotification, LikeNotification
from open_gallery.publications.exceptions import CommentNotFoundError, InvalidLikeError, InvalidUnlikeError
from open_gallery.shared.entity import Entity, EntityId, SubEntity
from open_gallery.tags.entities import Tag

PublicationId = NewType("PublicationId", EntityId)
CommentId = NewType("CommentId", EntityId)


@dataclass(kw_only=True)
class Comment(Entity):
    id: CommentId = field(default_factory=lambda: CommentId(EntityId.generate()))  # pyright: ignore[reportIncompatibleVariableOverride]
    text: str
    author: User
    children: list["Comment"] = field(default_factory=list)
    publication: "Publication" = field(repr=False)


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

    references: list["Publication"] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.views_count = len(self.views)

    def approve(self, actor: User) -> None:
        self.approved_by = actor

    def view(self, actor: User) -> None:
        self.views.append(View(user=actor))
        self.views_count += 1

    def get_like(self, actor: User) -> Like | None:
        return next((like for like in self.likes if like.user == actor), None)

    def like(self, actor: User) -> Like:
        existing_like = self.get_like(actor)
        if existing_like:
            raise InvalidLikeError(self.id)

        like = Like(user=actor)
        self.likes.append(like)
        self.likes_count += 1

        if actor != self.created_by:
            notification = LikeNotification(publication=self, actor=actor)
            self.created_by.notify(notification)
        return like

    def unlike(self, actor: User) -> None:
        existing_like = self.get_like(actor)
        if not existing_like:
            raise InvalidUnlikeError(self.id)

        self.likes.remove(existing_like)
        self.likes_count -= 1

    def get_comment(self, comment_id: CommentId) -> Comment | None:
        return next((comment for comment in self.comments if comment.id == comment_id), None)

    def add_comment(self, parent_id: CommentId | None, text: str, actor: User) -> Comment:
        comment = Comment(text=text, author=actor, publication=self)

        if not parent_id:
            self.comments.append(comment)
            self.comments_count += 1
        else:
            parent_comment = self.get_comment(parent_id)
            if not parent_comment:
                raise CommentNotFoundError(comment_id=parent_id)
            parent_comment.children.append(comment)
        if actor != self.created_by:
            notification = CommentNotification(publication=self, comment=comment, actor=actor)
            self.created_by.notify(notification)
        return comment

    def delete_comment(self, comment: Comment) -> None:
        self.comments.remove(comment)
        self.comments_count -= 1
