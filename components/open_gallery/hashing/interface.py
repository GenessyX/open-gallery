from abc import ABC, abstractmethod

type HashedValue = str


class Hasher(ABC):
    @abstractmethod
    def hash(self, value: str) -> HashedValue: ...

    @abstractmethod
    def verify(self, value: str, hashed_value: HashedValue) -> bool: ...


class SaltHasher(Hasher, ABC): ...
