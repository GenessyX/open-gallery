from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from open_gallery.shared.entity import EntityId
from open_gallery.shared.types import Email, SecretValue


def add_type_support(cls: type, json_schema: JsonSchemaValue) -> None:
    @classmethod  # type: ignore[misc]
    def _get_pydantic_core_schema__(
        cls: type,
        source_type: Any,  # noqa: ANN401, ARG001
        handler: GetCoreSchemaHandler,  # noqa: ARG001
    ) -> core_schema.PlainValidatorFunctionSchema:
        return core_schema.no_info_plain_validator_function(cls._validate_schema)  # type: ignore[attr-defined]

    @classmethod  # type: ignore[misc]
    def _validate_schema(
        cls: type,
        value: str,
    ) -> Any:  # noqa: ANN401
        if isinstance(value, cls):
            return value

        return cls(value)

    @classmethod  # type: ignore[misc]
    def _get_pydantic_json_schema__(
        cls: type,  # noqa: ARG001
        core_schema: CoreSchema,  # noqa: ARG001
        handler: GetJsonSchemaHandler,  # noqa: ARG001
    ) -> JsonSchemaValue:
        return json_schema

    cls._validate_schema = _validate_schema  # type: ignore[attr-defined]
    cls.__get_pydantic_core_schema__ = _get_pydantic_core_schema__  # type: ignore[attr-defined]
    cls.__get_pydantic_json_schema__ = _get_pydantic_json_schema__  # type: ignore[attr-defined]


def email_type_support() -> None:
    add_type_support(
        Email,
        {
            "type": "string",
            "format": "idn-email",
            "examples": [
                "test@example.com",
                "test2@test.ru",
            ],
        },
    )


def entity_id_type_support() -> None:
    add_type_support(
        EntityId,
        {
            "type": "string",
            "format": "uuid",
            "examples": [
                "067e7c31-8948-76a6-8000-d1ec0f8e7601",
                "067e7c31-816b-7a0c-8000-556388e86eca",
            ],
        },
    )


def secret_value_type_support() -> None:
    add_type_support(
        SecretValue,
        {
            "type": "string",
            "format": "password",
            "writeOnly": True,
        },
    )


def enable_types_support() -> None:
    email_type_support()
    entity_id_type_support()
    secret_value_type_support()
