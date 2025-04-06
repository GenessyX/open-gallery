from typing import override

from open_gallery.identity.entities import User, UserId, UserRole
from open_gallery.identity.exceptions import UserNotFoundError
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.shared.use_case import Usecase


class SetUserRoleUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, user_id: UserId, role: UserRole, actor: User) -> User:
        if actor.role is not UserRole.ADMIN:
            raise PermissionError
        async with self._uow as uow:
            user = await uow.users.get(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            user.role = role
            await uow.users.save(user)
        return user
