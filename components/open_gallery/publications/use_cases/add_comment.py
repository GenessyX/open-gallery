from open_gallery.identity.entities import User
from open_gallery.publications.entities import Comment, PublicationId
from open_gallery.publications.exceptions import PublicationNotFoundError
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class AddPublicationCommentUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, publication_id: PublicationId, text: str, actor: User) -> Comment:
        async with self._uow as uow:
            publication = await uow.publications.get(publication_id)

            if not publication:
                raise PublicationNotFoundError(publication_id)

            comment = publication.add_comment(text, actor)

            await uow.publications.save(publication)

        return comment
