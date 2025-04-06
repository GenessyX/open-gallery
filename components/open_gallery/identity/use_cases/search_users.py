from typing import override

from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import PermissionsError
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.shared.use_case import Usecase


class SearchUsersUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, email: str, actor: User) -> list[User]:
        if actor.role is not UserRole.ADMIN:
            raise PermissionsError
        async with self._uow as uow:
            return await uow.users.search("email", email)
