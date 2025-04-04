from typing import override

from open_gallery.hashing.interface import Hasher
from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.exceptions import InvalidCredentialsError
from open_gallery.identity.services.tokens import TokensService
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.shared.types import Email, SecretValue
from open_gallery.shared.use_case import Usecase


class LoginUserUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork, hasher: Hasher, tokens_service: TokensService) -> None:
        self._uow = uow
        self._hasher = hasher
        self._tokens_service = tokens_service

    @override
    async def __call__(self, email: Email, password: SecretValue[str]) -> TokensPair:
        async with self._uow as uow:
            user = await uow.users.get_by_email(email)
            if not user:
                raise InvalidCredentialsError

            valid_password = self._hasher.verify_password(
                password.get_secret_value(),
                user.password.get_secret_value(),
            )

            if not valid_password:
                raise InvalidCredentialsError

            return self._tokens_service.generate_tokens(user)
