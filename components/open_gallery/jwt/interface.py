import datetime
from abc import ABC, abstractmethod
from typing import TypeVar

from open_gallery.jwt.payload import JWTPayload

type SerializedToken = str

PayloadT = TypeVar("PayloadT", bound=JWTPayload)


class JWTService[PayloadT](ABC):
    @abstractmethod
    def encode(
        self,
        payload: PayloadT,
        expires_in: datetime.timedelta | None = None,
    ) -> SerializedToken: ...

    @abstractmethod
    def decode(self, serialized_token: SerializedToken) -> PayloadT: ...
