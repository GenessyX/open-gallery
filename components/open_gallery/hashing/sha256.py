import hashlib
from typing import override

from open_gallery.hashing.interface import Hasher


class Sha256Hasher(Hasher):
    @override
    def hash(self, value: str) -> str:
        m = hashlib.sha256(value.encode("utf-8"))
        return m.hexdigest()

    @override
    def verify(self, value: str, hashed_value: str) -> bool:
        expected_hash = self.hash(value)
        return expected_hash == hashed_value
