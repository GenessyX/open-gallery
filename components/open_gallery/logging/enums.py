from enum import Enum


class ContextCallType(str, Enum):
    REMOTE = "remote"
    INCOMING = "incoming"


class ContextEventType(str, Enum):
    REQUEST = "request"
    FAIL = "fail"
    RESPONSE = "response"
