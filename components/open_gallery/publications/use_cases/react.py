from open_gallery.identity.entities import User
from open_gallery.publications.dtos import ReactionType
from open_gallery.publications.entities import Like, PublicationId
from open_gallery.publications.exceptions import InvalidLikeError, InvalidUnlikeError, PublicationNotFoundError
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
            publication = await uow.publications.get(publication_id)

            if not publication:
                raise PublicationNotFoundError(publication_id)

            existing_like = next((like for like in publication.likes if like.user == actor), None)

            if reaction_type is ReactionType.UNLIKE:
                if not existing_like:
                    raise InvalidUnlikeError(publication_id)
                publication.likes.remove(existing_like)
            else:
                if existing_like:
                    raise InvalidLikeError(publication_id)
                like = Like(user=actor)
                publication.likes.append(like)

            await uow.publications.save(publication)

        return True
