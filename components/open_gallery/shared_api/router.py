import dataclasses
import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, override

from pydantic_core import PydanticUndefined

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


from fastapi import APIRouter as _APIRouter
from pydantic import BaseModel

from open_gallery.shared_api.model import APIModel


def transform_dataclass_to_response_model(cls: type["DataclassInstance"]) -> type[BaseModel]:
    class TransitModel(cls):  # type: ignore[valid-type, misc]
        pass

    for field_name, field_info in TransitModel.__dataclass_fields__.items():
        if hasattr(TransitModel, field_name):
            # NOTE: For some reason dataclass field with default value produces class attribute
            # with the name of field and value equal to default value.
            # So, for example:
            # ```
            # @dataclasses.dataclass
            # class Foo:
            #     bar: str = dataclasses.field(default="test")
            # ```
            # Will produce class Foo, with class attribute bar:
            # ```
            # assert Foo.bar == "test"
            # ```
            setattr(TransitModel, field_name, PydanticUndefined)
        if field_info.default:
            field_info.default = dataclasses.MISSING
        if field_info.default_factory:
            field_info.default_factory = dataclasses.MISSING

    return type(cls.__name__, (TransitModel, APIModel), {})


class APIRouter(_APIRouter):
    @override
    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = None,
        **kwargs: Any,
    ) -> None:
        if inspect.isclass(response_model) and dataclasses.is_dataclass(response_model):
            return super().add_api_route(
                path,
                endpoint,
                response_model=transform_dataclass_to_response_model(response_model),
                **kwargs,
            )
        return super().add_api_route(
            path,
            endpoint,
            response_model=response_model,
            **kwargs,
        )
