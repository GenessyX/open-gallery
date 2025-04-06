from typing import override

from open_gallery.identity.entities import User
from open_gallery.publications.entities import Publication, PublicationId, View
from open_gallery.publications.exceptions import PublicationNotFoundError
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class GetPublicationUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, publication_id: PublicationId, actor: User) -> Publication:
        async with self._uow as uow:
            publication = await uow.publications.get(publication_id)

            if not publication:
                raise PublicationNotFoundError(publication_id)

            already_viewed = next((view for view in publication.views if view.user == actor), None)
            if not already_viewed:
                publication.views.append(View(user=actor))
                await uow.publications.save(publication)

        return publication
