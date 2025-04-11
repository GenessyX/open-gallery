from typing import TYPE_CHECKING

from open_gallery.shared.exceptions import DomainError

if TYPE_CHECKING:
    from open_gallery.publications.entities import PublicationId


class PublicationError(DomainError): ...


class InvalidImagesInPublicationError(PublicationError):
    message_template = "The publication has non-existent images"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class PublicationNotFoundError(PublicationError):
    message_template = "Publication with id {publication_id} not found"

    def __init__(self, publication_id: "PublicationId") -> None:
        super().__init__(self.message_template.format(publication_id=publication_id))


class InvalidUnlikeError(PublicationError):
    message_template = "You have no like on publication with id {publication_id}"

    def __init__(self, publication_id: "PublicationId") -> None:
        super().__init__(self.message_template.format(publication_id=publication_id))


class InvalidLikeError(PublicationError):
    message_template = "You have already liked publication with id {publication_id}"

    def __init__(self, publication_id: "PublicationId") -> None:
        super().__init__(self.message_template.format(publication_id=publication_id))
