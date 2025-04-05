from typing import override

from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.exceptions import InvalidCredentialsError
from open_gallery.identity.services.tokens import TokensService
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.jwt.interface import SerializedToken
from open_gallery.shared.types import SecretValue
from open_gallery.shared.use_case import Usecase


class RefreshTokenUsecase(Usecase):
    def __init__(
        self,
        uow: IdentityUnitOfWork,
        tokens_service: TokensService,
    ) -> None:
        self._uow = uow
        self._tokens_service = tokens_service

    @override
    async def __call__(self, token: SecretValue[SerializedToken]) -> TokensPair:
        async with self._uow as uow:
            old_hashed_refresh_token = self._tokens_service.get_refresh_token_hash(token.get_secret_value())
            user = await uow.users.get_by_refresh_token(SecretValue(old_hashed_refresh_token))

            if not user:
                raise InvalidCredentialsError

            tokens = self._tokens_service.generate_tokens(user)

            hashed_refresh_token = self._tokens_service.get_refresh_token_hash(tokens.refresh_token)
            user.add_refresh_token(hashed_refresh_token)
            user.delete_refresh_token(old_hashed_refresh_token)

            await uow.users.save(user)

        return tokens
