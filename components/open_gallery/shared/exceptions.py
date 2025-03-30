from typing import ClassVar


class DomainError(Exception):
    message_template: ClassVar[str] = "error message"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
