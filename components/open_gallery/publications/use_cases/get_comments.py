from typing import override

from open_gallery.publications.entities import Comment, PublicationId
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class GetPublicationCommentsUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, publication_id: PublicationId, limit: int, offset: int) -> list[Comment]:
        async with self._uow as uow:
            return await uow.publications.get_comments(publication_id, limit, offset)
