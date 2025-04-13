from open_gallery.publications.dtos import ReactionType
from open_gallery.publications.entities import CommentId
from open_gallery.shared_api.model import APIModel


class AddPublicationCommentRequestSchema(APIModel):
    text: str
    parent_id: CommentId | None = None


class ReactToPublicationRequestSchema(APIModel):
    reaction_type: ReactionType
