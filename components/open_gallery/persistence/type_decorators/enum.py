from enum import Enum
from typing import TYPE_CHECKING, Generic, TypeVar, cast

from sqlalchemy import ARRAY

if TYPE_CHECKING:
    from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.sqltypes import (
    String,
)
from sqlalchemy.sql.type_api import TypeDecorator

EnumT = TypeVar("EnumT", bound=Enum)


class StrEnumTypeImpl(TypeDecorator[EnumT]):
    cache_ok = True
    impl = String
    target: type[EnumT]

    def process_result_value(
        self,
        value: str | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> EnumT | None:
        if value is None:
            return None
        return self.target(value)

    def process_bind_param(
        self,
        value: EnumT | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> str | None:
        if value is None:
            return None
        return cast("str", value.value)


class StrEnumArrayTypeImpl(TypeDecorator[list[EnumT]], Generic[EnumT]):
    cache_ok = True
    impl = ARRAY(String)
    target: type[EnumT]

    def process_result_value(
        self,
        value: list[str] | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> list[EnumT]:
        if value is None:
            return []
        return [self.target(v) for v in value]

    def process_bind_param(
        self,
        value: list[EnumT] | None,
        dialect: "Dialect",  # noqa: ARG002
    ) -> list[str]:
        if value is None:
            return []
        return [v.value for v in value]
