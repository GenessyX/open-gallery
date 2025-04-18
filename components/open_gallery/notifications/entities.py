from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from open_gallery.shared.entity import Entity

if TYPE_CHECKING:
    from open_gallery.identity.entities import User
    from open_gallery.publications.entities import Comment, Publication


class NotificationType(str, Enum):
    LIKE = "like"
    COMMENT = "comment"
    LINKED = "linked"


@dataclass(kw_only=True)
class Notification(Entity):
    type: NotificationType
    publication: "Publication"
    actor: "User"
    seen: bool = False


@dataclass(kw_only=True)
class CommentNotification(Notification):
    type: NotificationType = NotificationType.COMMENT
    comment: "Comment"


@dataclass(kw_only=True)
class LikeNotification(Notification):
    type: NotificationType = NotificationType.LIKE


GenericNotification = CommentNotification | LikeNotification
