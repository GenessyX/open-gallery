import datetime
from typing import override

from open_gallery.publications.entities import Publication
from open_gallery.publications.uow import PublicationsUnitOfWork
from open_gallery.shared.use_case import Usecase


class GetPopularPublicationsUsecase(Usecase):
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, limit: int) -> list[Publication]:
        async with self._uow as uow:
            return await uow.publications.get_popular(limit, since=datetime.timedelta(hours=24))
