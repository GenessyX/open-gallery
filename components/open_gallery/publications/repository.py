from abc import ABC, abstractmethod

from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.shared.repository import Repository


class PublicationRepository(Repository[PublicationId, Publication], ABC):
    @abstractmethod
    async def get_not_approved(self, limit: int, offset: int) -> list[Publication]: ...
