from collections.abc import Callable
from http import HTTPStatus
from typing import Any, TypeVar, assert_never

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from open_gallery.shared.exceptions import DomainError
from open_gallery.shared_api.model import APIModel


class APIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)


class APIErrorSchema(APIModel):
    detail: Any


def api_error_handler(_: Request, exc: APIError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=APIErrorSchema(
            detail=exc.message,
        ).model_dump(by_alias=True),
    )


ExceptionT = TypeVar("ExceptionT", bound=Exception)


def to_exception_handler(
    handler: Callable[[Request, ExceptionT], APIError],
) -> Callable[[Request, ExceptionT], Response]:
    def wrapped_handler(request: Request, exc: ExceptionT) -> Response:
        api_error = handler(request, exc)
        return api_error_handler(request, api_error)

    return wrapped_handler


def domain_error_handler(_: Request, exception: DomainError) -> APIError:
    match exception:
        case DomainError():
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        case _:
            assert_never()

    return APIError(
        status_code=status_code,
        message=exception.message,
    )


def define_possible_errors(
    exceptions_map: dict[int, type[DomainError]],
) -> Any:  # noqa: ANN401
    out_map = {}
    for status_code, exception in exceptions_map.items():
        out_map[status_code] = {
            "description": exception.__name__,
            "content": {"application/json": {"example": {"detail": exception.message_template}}},
        }
    return out_map
