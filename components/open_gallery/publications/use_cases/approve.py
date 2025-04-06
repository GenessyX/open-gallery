from typing import override

from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import PermissionsError
from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.publications.exceptions import PublicationNotFoundError
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class ApprovePublicationUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, publication_id: PublicationId, actor: User) -> Publication:
        if actor.role not in (UserRole.ADMIN, UserRole.MODERATOR):
            raise PermissionsError
        async with self._uow as uow:
            publication = await uow.publications.get(publication_id)
            if not publication:
                raise PublicationNotFoundError(publication_id)

            publication.approve(actor)
            await uow.publications.save(publication)

        return publication
