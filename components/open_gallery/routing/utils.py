import mimetypes

import orjson
from fastapi import UploadFile
from starlette.datastructures import ImmutableMultiDict

from open_gallery.http_utils.core import (
    convert_body,
    convert_mapping,
    get_content_type,
)


def convert_fastapi_multi_mapping(multi_mapping: ImmutableMultiDict[str, str]) -> str:
    return orjson.dumps(multi_mapping.multi_items()).decode("utf-8")


def get_file_extension(file: UploadFile) -> str | None:
    if file.filename:
        splitted = file.filename.split(".")
        if len(splitted) > 1:
            return splitted[-1]
    if file.content_type:
        guessed = mimetypes.guess_extension(file.content_type)
        if guessed:
            return guessed.lstrip(".")
    return None


__all__ = [
    "convert_body",
    "convert_fastapi_multi_mapping",
    "convert_mapping",
    "get_content_type",
    "get_file_extension",
]
