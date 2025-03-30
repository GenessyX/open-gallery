from typing import override

from open_gallery.passwords.complexity.interface import PasswordComplexityVerifier


class LengthBasedVerifier(PasswordComplexityVerifier):
    def __init__(self, length: int = 8) -> None:
        self._length = length

    @override
    def verify(self, password: str) -> bool:
        return len(password) >= self._length
