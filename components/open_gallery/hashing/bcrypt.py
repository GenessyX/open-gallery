import os
from typing import override

from argon2 import PasswordHasher

from open_gallery.hashing.interface import Hasher


class Argon2Hasher(Hasher):
    def __init__(self) -> None:
        self._argon = PasswordHasher()

    @override
    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        return self._argon.hash(password, salt=salt)

    @override
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self._argon.verify(hash=hashed_password, password=password)
