from abc import ABC, abstractmethod


class Hasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool: ...
