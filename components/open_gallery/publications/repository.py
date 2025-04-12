from abc import ABC, abstractmethod

from open_gallery.identity.entities import UserId
from open_gallery.publications.entities import Comment, CommentId, Publication, PublicationId
from open_gallery.shared.repository import Repository


class PublicationRepository(Repository[PublicationId, Publication], ABC):
    @abstractmethod
    async def get_not_approved(self, limit: int, offset: int) -> list[Publication]: ...

    @abstractmethod
    async def get_with_views(self, publication_id: PublicationId, user_id: UserId) -> Publication | None: ...

    @abstractmethod
    async def get_with_likes(self, publication_id: PublicationId, user_id: UserId) -> Publication | None: ...

    @abstractmethod
    async def get_comments(self, publication_id: PublicationId, limit: int, offset: int) -> list[Comment]: ...

    @abstractmethod
    async def get_with_comment(self, publication_id: PublicationId, comment_id: CommentId) -> Publication | None: ...
