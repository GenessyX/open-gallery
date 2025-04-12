from open_gallery.shared.exceptions import DomainError


class UploadError(DomainError): ...


class InvalidFileError(UploadError):
    message_template = "Attempting to upload invalid file"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class TooLargeFileError(UploadError):
    message_template = "File size limit is {limit} bytes"

    def __init__(self, limit: int) -> None:
        super().__init__(self.message_template.format(limit=limit))
