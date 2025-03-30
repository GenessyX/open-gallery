import dataclasses
from abc import ABC
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, cast

from dishka import BaseScope, Component, Provider, Scope
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


class BaseSettingsProvider(Provider, ABC):
    root_settings: type[BaseSettings] | type["DataclassInstance"]
    scope = Scope.RUNTIME
    base: bool = True

    def __init__(
        self,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        super().__init__(scope, component)

        if self.base:

            def base_settings() -> BaseSettings:
                return cast("BaseSettings", self.root_settings())

            self.provide(base_settings, provides=self.root_settings)

        settings = self.root_settings
        if not dataclasses.is_dataclass(settings):
            for field_name, field_info in self.root_settings.model_fields.items():  # type: ignore[union-attr]

                def create_provider(field_name: str = field_name) -> Callable[[BaseSettings], Any]:
                    def _provider(base_settings: BaseSettings) -> Any:  # noqa: ANN401
                        return getattr(base_settings, field_name)

                    _provider.__annotations__["base_settings"] = self.root_settings

                    return _provider

                self.provide(create_provider(field_name), provides=field_info.annotation)
        else:
            for field in dataclasses.fields(settings):

                def create_provider(field_name: str = field.name) -> Callable[[BaseSettings], Any]:
                    def _provider(base_settings: BaseSettings) -> Any:  # noqa: ANN401
                        return getattr(base_settings, field_name)

                    _provider.__annotations__["base_settings"] = self.root_settings

                    return _provider

                self.provide(create_provider(field.name), provides=field.type)
