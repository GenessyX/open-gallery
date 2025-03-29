import re
from typing import override


class Email(str):
    __slots__ = ()

    def __new__(cls, address: str) -> "Email":
        cls._validate(address)
        return super().__new__(cls, address)

    @staticmethod
    def _validate(address: str) -> None:
        """Validate the email address."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, address):
            msg = f"Invalid email address: {address}"
            raise ValueError(msg)


class SecretValue[T]:
    def __init__(self, secret_value: T) -> None:
        self._secret_value = secret_value

    def _display(self) -> str:
        return "********" if self._secret_value else ""

    def get_secret_value(self) -> T:
        return self._secret_value

    @override
    def __str__(self) -> str:
        return self._display()

    @override
    def __repr__(self) -> str:
        return self._display()

    @override
    def __eq__(self, other: object, /) -> bool:
        return isinstance(other, self.__class__) and self.get_secret_value() == other.get_secret_value()

    @override
    def __hash__(self) -> int:
        return hash(self.get_secret_value())
