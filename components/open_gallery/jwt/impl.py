import datetime
import json
from typing import Literal, cast, override

from adaptix import Retort, dumper, loader
from jwcrypto.common import JWException
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT, JWTExpired

from open_gallery.jwt.exceptions import ExpiredTokenError, TokenDecodeError
from open_gallery.jwt.interface import JWTService, PayloadT, SerializedToken

retort = Retort(
    recipe=[
        dumper(
            datetime.datetime,
            lambda x: int(x.timestamp()),
        ),
        loader(
            datetime.datetime,
            lambda x: datetime.datetime.fromtimestamp(x, tz=datetime.UTC),
        ),
    ],
)


type Algorithm = Literal["HS256", "RS256"]


class JwcryptoJWTService(JWTService[PayloadT]):
    def __init__(self, secret: str, algorithm: Algorithm, payload_type: type[PayloadT]) -> None:
        self._secret = secret
        self._key = JWK.from_password(secret)
        self._algorithm = algorithm
        self._payload_type = payload_type

    @override
    def encode(
        self,
        payload: PayloadT,
        expires_in: datetime.timedelta | None = None,
    ) -> SerializedToken:
        if expires_in is not None:
            payload.exp = payload.iat + expires_in

        token = JWT(
            header={"alg": self._algorithm, "typ": "JWT"},
            claims=retort.dump(payload),
        )
        token.make_signed_token(key=self._key)
        return cast("SerializedToken", token.serialize())

    @override
    def decode(self, serialized_token: SerializedToken) -> PayloadT:
        try:
            token = JWT(jwt=serialized_token, key=self._key, expected_type="JWS")
        except JWTExpired as err:
            raise ExpiredTokenError from err
        except (JWException, ValueError) as err:
            raise TokenDecodeError from err

        return retort.load(
            json.loads(token.claims),
            self._payload_type,
        )
