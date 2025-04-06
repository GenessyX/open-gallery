import dataclasses
import inspect
import typing
from collections.abc import Callable
from types import UnionType
from typing import TYPE_CHECKING, Any, Union, cast, get_origin, override

from fastapi import APIRouter as _APIRouter
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from open_gallery.shared.types import SecretValue
from open_gallery.shared_api.model import APIModel

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


def create_fields(cls: type["DataclassInstance"]) -> list[tuple[str, type | Any, Any]]:
    field_defs: list[tuple[str, type | Any, Any]] = []
    for field in dataclasses.fields(cls):
        if get_origin(field.type) is SecretValue or field.metadata.get("exclude", False) or not field.repr:
            continue

        origin = typing.get_origin(field.type)
        if origin:
            if origin is UnionType:
                origin = Union
            overwrite_args = []
            generic_args = typing.get_args(field.type)
            for arg in generic_args:
                if inspect.isclass(arg) and dataclasses.is_dataclass(arg):
                    _arg = transform_dataclass_to_response_model(arg)
                else:
                    _arg = arg
                overwrite_args.append(_arg)
            type_ = origin[*overwrite_args]
        elif inspect.isclass(field.type) and dataclasses.is_dataclass(field.type):
            type_ = transform_dataclass_to_response_model(field.type)
        else:
            type_ = field.type

        field_defs.append(
            (
                field.name,
                type_,
                field.default if field.default is not field.default_factory else field.default_factory,
            ),
        )
    return field_defs


def transform_dataclass_to_response_model(cls: type["DataclassInstance"]) -> type[BaseModel]:
    field_defs = create_fields(cls)

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


def transform_response_model(cls: type) -> type:
    if inspect.isclass(cls) and dataclasses.is_dataclass(cls):
        return transform_dataclass_to_response_model(cls)
    origin = typing.get_origin(cls)
    if not origin:
        return cls

    overwrite_args = []
    generic_args = typing.get_args(cls)
    for arg in generic_args:
        if inspect.isclass(arg) and dataclasses.is_dataclass(arg):
            _arg = transform_dataclass_to_response_model(arg)
        else:
            _arg = arg
        overwrite_args.append(_arg)

    return cast("type", origin[*overwrite_args])


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
        response_model = transform_response_model(response_model)
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
