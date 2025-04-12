from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from open_gallery.shared.entity import Entity

if TYPE_CHECKING:
    from open_gallery.identity.entities import User
    from open_gallery.publications.entities import Comment, Like, Publication


class NotificationType(str, Enum):
    LIKE = "like"
    COMMENT = "comment"
    LINKED = "linked"


@dataclass(kw_only=True)
class Notification(Entity):
    type: NotificationType
    publication: "Publication"
    actor: "User"


@dataclass(kw_only=True)
class CommentNotification(Notification):
    comment: "Comment"


@dataclass(kw_only=True)
class LikeNotification(Notification):
    like: "Like"
