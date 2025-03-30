from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import registry

from open_gallery.persistence.type_decorators.datetime import UTCDateTime

mapper_registry = registry()

if TYPE_CHECKING:
    import datetime

    from sqlalchemy.sql.schema import Column
else:
    from sqlalchemy.sql.schema import Column as _Column

    class Column(_Column):
        inherit_cache = True

        def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
            kwargs.setdefault("nullable", False)
            super().__init__(*args, **kwargs)


def datetime_columns() -> list["Column[datetime.datetime]"]:
    return [
        Column("created_at", UTCDateTime, server_default=func.now()),
        Column("updated_at", UTCDateTime, server_default=func.now()),
    ]


__all__ = ["Column"]
