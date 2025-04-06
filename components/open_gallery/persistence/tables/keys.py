from collections.abc import Callable

from sqlalchemy import UUID, ForeignKey

type _ForeignKey = Callable[[], ForeignKey]

UserPrimaryKeyType = UUID
UserForeignKey: _ForeignKey = lambda: ForeignKey("users.id", ondelete="CASCADE")  # noqa: E731

ImagePrimaryKeyType = UUID
ImageForeignKey: _ForeignKey = lambda: ForeignKey("images.id", ondelete="CASCADE")  # noqa: E731

PublicationPrimaryKeyType = UUID
PublicationForeignKey: _ForeignKey = lambda: ForeignKey("publications.id", ondelete="CASCADE")  # noqa: E731

PublicationCommentPrimaryKeyType = UUID
PublicationCommentForeignKey: _ForeignKey = lambda: ForeignKey("publication_comments.id", ondelete="CASCADE")  # noqa: E731

TagPrimaryKeyType = UUID
TagForeignKey: _ForeignKey = lambda: ForeignKey("tags.id", ondelete="CASCADE")  # noqa: E731
