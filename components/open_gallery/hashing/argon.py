import os
from typing import override

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from open_gallery.hashing.interface import SaltHasher


class Argon2Hasher(SaltHasher):
    def __init__(self) -> None:
        self._argon = PasswordHasher()

    @override
    def hash(self, value: str) -> str:
        salt = os.urandom(16)
        return self._argon.hash(value, salt=salt)

    @override
    def verify(self, value: str, hashed_value: str) -> bool:
        try:
            return self._argon.verify(hash=hashed_value, password=value)
        except VerifyMismatchError:
            return False
