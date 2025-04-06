from open_gallery.shared.exceptions import DomainError
from open_gallery.tags.entities import TagId


class TagError(DomainError): ...


class TagNotFoundError(TagError):
    message_template = "Tag with id {tag_id} not found"

    def __init__(self, tag_id: TagId) -> None:
        super().__init__(self.message_template.format(tag_id=tag_id))
