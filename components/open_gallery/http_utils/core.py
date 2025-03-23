import email.message
from collections.abc import Mapping, Sequence

import orjson

from open_gallery.http_utils.constants import BINARY_LOG_STATIC, HR_CONTENT_TYPES


def get_content_type(headers: Mapping[str, str]) -> str:
    content_type = headers.get("content-type")
    if not content_type:
        return ""
    msg = email.message.Message()
    msg["content-type"] = content_type
    return msg.get_content_type()


def convert_body(content_type: str, body: bytes) -> str:
    if not body:
        return ""
    if content_type not in HR_CONTENT_TYPES:
        return BINARY_LOG_STATIC
    return body.decode("utf-8")


def convert_mapping(mapping: Mapping[str, str | Sequence[str]]) -> str:
    return orjson.dumps(mapping).decode("utf-8")
