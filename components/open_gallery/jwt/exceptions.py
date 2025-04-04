from open_gallery.shared.exceptions import DomainError


class JWTError(DomainError):
    message_template = "Failed to decode JWT"

    def __init__(self) -> None:
        super().__init__(self.message_template)
