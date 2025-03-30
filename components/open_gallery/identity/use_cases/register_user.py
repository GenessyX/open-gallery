from typing import override

from open_gallery.hashing.interface import Hasher
from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import UserExistsError, WeakPasswordError
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
    ) -> None:
        self._uow = uow
        self._hasher = hasher
        self._verifier = verifier

    @override
    async def __call__(self, email: Email, password: SecretValue[str]) -> User:
        async with self._uow as uow:
            existing = await uow.users.get_by_email(email=email)
            if existing:
                raise UserExistsError(email)

            if not self._verifier.verify(password.get_secret_value()):
                raise WeakPasswordError

            hashed_password = self._hasher.hash_password(password.get_secret_value())
            user = User(
                email=email,
                password=SecretValue(hashed_password),
                role=UserRole.USER,
            )
            await uow.users.save(user)
        return user
