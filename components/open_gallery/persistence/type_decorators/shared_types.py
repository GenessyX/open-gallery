from typing import override

from sqlalchemy import Dialect, String, TypeDecorator

from open_gallery.shared.types import SecretValue


class SecretValueTypeImpl(TypeDecorator[SecretValue[str]]):
    impl = String
    cache_ok = True

    @override
    def process_bind_param(self, value: SecretValue[str] | None, dialect: Dialect) -> str | None:
        if value is None:
            return None
        return value.get_secret_value()

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> SecretValue[str] | None:
        if value is None:
            return None
        return SecretValue(value)
