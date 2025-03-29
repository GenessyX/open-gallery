from typing import override

from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.shared.types import Email, SecretValue
from open_gallery.shared.use_case import Usecase


class RegisterUserUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, email: str, password: str) -> User:
        async with self._uow as uow:
            user = User(
                email=Email(email),
                password=SecretValue(password),
                role=UserRole.USER,
            )
            await uow.users.save(user)
        return user
