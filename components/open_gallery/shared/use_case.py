from abc import ABC, abstractmethod
from typing import Any


class Usecase(ABC):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> Any: ...  # noqa: ANN401
