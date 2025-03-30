import dataclasses
import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, cast, get_origin, override

from pydantic_core import PydanticUndefined

from open_gallery.shared.types import SecretValue

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


from fastapi import APIRouter as _APIRouter
from pydantic import BaseModel

from open_gallery.shared_api.model import APIModel


def transform_dataclass_to_response_model(cls: type["DataclassInstance"]) -> type[BaseModel]:
    field_defs = [
        (f.name, f.type, f.default if f.default is not f.default_factory else f.default_factory)
        for f in dataclasses.fields(cls)
        if get_origin(f.type) is not SecretValue
    ]

    TransitModel = cast(  # noqa: N806
        "type[DataclassInstance]",
        dataclasses.make_dataclass(
            "TransitModel",
            field_defs,
            kw_only=True,
        ),
    )

    for field_name, field_info in TransitModel.__dataclass_fields__.items():
        if hasattr(TransitModel, field_name):
            # NOTE: For some reason dataclass field with default value produces class attribute
            # with the name of field and value equal to default value, and Pydantic tries to
            # get all attributes on model to identify if default value is set.
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
        response_model = response_model or endpoint.__annotations__.get("return", str)
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
