from open_gallery.publications.entities import Publication
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class GetPublicationsListUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> list[Publication]:
        async with self._uow as uow:
            return await uow.publications.get_list(limit, offset)
