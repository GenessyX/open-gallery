from typing import override

from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import PermissionsError
from open_gallery.publications.entities import Publication
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class GetNotApprovedPublicationsUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, limit: int, offset: int, actor: User) -> list[Publication]:
        if actor.role not in (UserRole.MODERATOR, UserRole.ADMIN):
            raise PermissionsError
        async with self._uow as uow:
            return await uow.publications.get_not_approved(limit, offset)
