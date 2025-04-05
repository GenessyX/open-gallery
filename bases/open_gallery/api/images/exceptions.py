from http import HTTPStatus

from fastapi import Request

from open_gallery.images.exceptions import InvalidFileError, UploadError
from open_gallery.shared_api.exceptions import APIError, to_exception_handler


@to_exception_handler
def upload_error_handler(_: Request, exception: UploadError) -> APIError:
    match exception:
        case InvalidFileError():
            status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        case _:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return APIError(
        status_code=status_code,
        message=exception.message,
    )
