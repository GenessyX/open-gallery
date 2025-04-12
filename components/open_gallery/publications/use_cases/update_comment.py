from typing import override

from open_gallery.identity.entities import User, UserRole
from open_gallery.identity.exceptions import PermissionsError
from open_gallery.publications.entities import Comment, CommentId, PublicationId
from open_gallery.publications.exceptions import CommentNotFoundError, PublicationNotFoundError
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class UpdatePublicationCommentUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(
        self,
        publication_id: PublicationId,
        comment_id: CommentId,
        text: str,
        actor: User,
    ) -> Comment:
        async with self._uow as uow:
            publication = await uow.publications.get_with_comment(publication_id, comment_id)

            if not publication:
                raise PublicationNotFoundError(publication_id)

            comment = publication.get_comment(comment_id)

            # comment = await uow.comments.get(comment_id)
            if not comment:
                raise CommentNotFoundError(comment_id)

            if actor.role is not UserRole.ADMIN and comment.author != actor:
                raise PermissionsError

            comment.text = text

            await uow.publications.save(publication)
            # await uow.comments.save(comment)

        return comment
