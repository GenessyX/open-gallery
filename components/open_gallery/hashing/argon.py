import os
from typing import override

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from open_gallery.hashing.interface import Hasher


class Argon2Hasher(Hasher):
    def __init__(self) -> None:
        self._argon = PasswordHasher()

    @override
    def hash(self, password: str) -> str:
        salt = os.urandom(16)
        return self._argon.hash(password, salt=salt)

    @override
    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            return self._argon.verify(hash=hashed_password, password=password)
        except VerifyMismatchError:
            return False
