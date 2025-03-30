from open_gallery.shared.exceptions import DomainError


class UserError(DomainError): ...


class UserExistsError(UserError):
    message_template = "User with email {email} already exists"

    def __init__(self, email: str) -> None:
        super().__init__(self.message_template.format(email=email))
