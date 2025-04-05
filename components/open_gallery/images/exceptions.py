from open_gallery.shared.exceptions import DomainError


class UploadError(DomainError): ...


class InvalidFileError(UploadError):
    message_template = "Attempting to upload invalid file"

    def __init__(self) -> None:
        super().__init__(self.message_template)
