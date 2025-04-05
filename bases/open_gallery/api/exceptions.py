from http import HTTPStatus

from fastapi import Request

from open_gallery.jwt.exceptions import ExpiredTokenError, JWTError, TokenDecodeError
from open_gallery.shared_api.exceptions import APIError, to_exception_handler


@to_exception_handler
def jwt_error_handler(_: Request, exception: JWTError) -> APIError:
    match exception:
        case TokenDecodeError() | ExpiredTokenError():
            status_code = HTTPStatus.UNAUTHORIZED
        case _:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return APIError(
        status_code=status_code,
        message=exception.message,
    )
