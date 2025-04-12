from typing import override

from open_gallery.identity.entities import User
from open_gallery.identity.uow import IdentityUnitOfWork
from open_gallery.notifications.entities import GenericNotification
from open_gallery.shared.use_case import Usecase


class GetUserNotificationsUsecase(Usecase):
    def __init__(self, uow: IdentityUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, actor: User, limit: int = 20, offset: int = 0) -> list[GenericNotification]:
        async with self._uow as uow:
            return await uow.users.get_notifications(actor.id, limit, offset)
