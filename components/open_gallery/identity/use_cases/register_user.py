from typing import override

from open_gallery.hashing.interface import Hasher
from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import UserExistsError, WeakPasswordError
from open_gallery.identity.services.tokens import TokensService
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.passwords.complexity.interface import PasswordComplexityVerifier
from open_gallery.shared.types import Email, SecretValue
from open_gallery.shared.use_case import Usecase


class RegisterUserUsecase(Usecase):
    def __init__(
        self,
        uow: IdentityUnitOfWork,
        hasher: Hasher,
        verifier: PasswordComplexityVerifier,
        tokens_service: TokensService,
    ) -> None:
        self._uow = uow
        self._hasher = hasher
        self._verifier = verifier
        self._tokens_service = tokens_service

    @override
    async def __call__(self, email: Email, password: SecretValue[str]) -> TokensPair:
        async with self._uow as uow:
            existing = await uow.users.get_by_email(email=email)
            if existing:
                raise UserExistsError(email)

            if not self._verifier.verify(password.get_secret_value()):
                raise WeakPasswordError

            hashed_password = self._hasher.hash(password.get_secret_value())
            user = User(
                email=email,
                password=SecretValue(hashed_password),
                role=UserRole.USER,
            )

            tokens_pair = self._tokens_service.generate_tokens(user)

            hashed_refresh_token = self._hasher.hash(tokens_pair.refresh_token)

            user.add_refresh_token(hashed_refresh_token)

            await uow.users.save(user)

        return tokens_pair
