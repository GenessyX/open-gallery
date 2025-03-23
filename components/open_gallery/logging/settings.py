from dataclasses import dataclass
from enum import Enum


class LoggingFormatter(str, Enum):
    PLAIN = "plain"
    JSON = "json"


@dataclass(kw_only=True)
class LoggingSettings:
    formatter: LoggingFormatter = LoggingFormatter.PLAIN
    root_level: str = "ERROR"
    handlers_level: str = "INFO"
