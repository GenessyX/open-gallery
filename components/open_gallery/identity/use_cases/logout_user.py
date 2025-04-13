from typing import override

from open_gallery.identity.dtos import RefreshTokenPayload
from open_gallery.identity.exceptions import InvalidCredentialsError
from open_gallery.identity.services.tokens import TokensService
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.jwt.interface import JWTService, SerializedToken
from open_gallery.shared.types import SecretValue
from open_gallery.shared.use_case import Usecase


class LogoutUserUsecase(Usecase):
    def __init__(
        self,
        uow: IdentityUnitOfWork,
        tokens_service: TokensService,
        jwt_service: JWTService[RefreshTokenPayload],
    ) -> None:
        self._uow = uow
        self._tokens_service = tokens_service
        self._jwt_service = jwt_service

    @override
    async def __call__(self, token: SecretValue[SerializedToken]) -> None:
        async with self._uow as uow:
            self._jwt_service.decode(token.get_secret_value())
            refresh_token_hash = self._tokens_service.get_refresh_token_hash(token.get_secret_value())
            user = await uow.users.get_by_refresh_token(refresh_token_hash)

            if not user:
                raise InvalidCredentialsError

            user.delete_refresh_token(refresh_token_hash)

            await uow.users.save(user)
