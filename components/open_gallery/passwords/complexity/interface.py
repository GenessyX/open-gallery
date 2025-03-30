from abc import ABC, abstractmethod


class PasswordComplexityVerifier(ABC):
    @abstractmethod
    def verify(self, password: str) -> bool: ...
