from open_gallery.identity.entities import User
from open_gallery.publications.dtos import ReactionType
from open_gallery.publications.entities import PublicationId
from open_gallery.publications.exceptions import PublicationNotFoundError
from open_gallery.publications.uow import PublicationsUnitOfWork


class ReactToPublicationUsecase:
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    async def __call__(
        self,
        publication_id: PublicationId,
        reaction_type: ReactionType,
        actor: User,
    ) -> bool:
        async with self._uow as uow:
            publication = await uow.publications.get_with_likes(publication_id, actor.id)

            if not publication:
                raise PublicationNotFoundError(publication_id)

            match reaction_type:
                case ReactionType.LIKE:
                    publication.like(actor)
                case ReactionType.UNLIKE:
                    publication.unlike(actor)

            await uow.publications.save(publication)

        return True
