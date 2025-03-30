from http import HTTPStatus

from fastapi import Request

from open_gallery.identity.exceptions import UserError, UserExistsError
from open_gallery.shared_api.exceptions import APIError, to_exception_handler


@to_exception_handler
def user_error_handler(_: Request, exception: UserError) -> APIError:
    match exception:
        case UserExistsError():
            status_code = HTTPStatus.CONFLICT
        case _:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return APIError(
        status_code=status_code,
        message=exception.message,
    )
