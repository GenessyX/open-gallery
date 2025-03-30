from collections.abc import Callable

from sqlalchemy import UUID, ForeignKey

type _ForeignKey = Callable[[], ForeignKey]

UserPrimaryKeyType = UUID
UserForeignKey: _ForeignKey = lambda: ForeignKey("users.id", ondelete="CASCADE")  # noqa: E731
