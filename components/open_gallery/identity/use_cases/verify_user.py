from typing import override

from open_gallery.identity.exceptions import InvalidCredentialsError
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.shared.use_case import Usecase


class VerifyUserUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, code: str) -> bool:
        async with self._uow as uow:
            user = await uow.users.get_by_code(code)

            if not user:
                raise InvalidCredentialsError

            is_valid = user.verify(code)

            if not is_valid:
                raise InvalidCredentialsError

            await uow.users.save(user)

        return True
