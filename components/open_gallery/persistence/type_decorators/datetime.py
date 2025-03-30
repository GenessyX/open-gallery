import datetime
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import DateTime, TypeDecorator

if TYPE_CHECKING:
    from sqlalchemy.engine.interfaces import Dialect

LOCAL_UTC_OFFSET = datetime.datetime.now().astimezone().utcoffset()
LOCAL_TIMEZONE = datetime.timezone(LOCAL_UTC_OFFSET) if LOCAL_UTC_OFFSET else datetime.UTC


class UTCDateTime(TypeDecorator[datetime.datetime]):
    impl = DateTime
    cache_ok = True

    @property
    def python_type(self) -> type[Any]:
        return cast("type", self.impl.python_type)

    def process_bind_param(
        self,
        value: datetime.datetime | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> datetime.datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.astimezone(LOCAL_TIMEZONE)
        return value.astimezone(datetime.UTC).replace(tzinfo=None)

    def process_result_value(
        self,
        value: datetime.datetime | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> datetime.datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.UTC)
        return value.astimezone(datetime.UTC)
