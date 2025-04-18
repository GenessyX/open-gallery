from open_gallery.identity.entities import UserId
from open_gallery.shared.exceptions import DomainError


class UserError(DomainError): ...


class UserExistsError(UserError):
    message_template = "User with email {email} already exists"

    def __init__(self, email: str) -> None:
        super().__init__(self.message_template.format(email=email))


class WeakPasswordError(UserError):
    message_template = "Password is too weak"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class AuthorizationError(UserError):
    message_template = "Not authenticated"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class InvalidCredentialsError(UserError):
    message_template = "Invalid credentials"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class PermissionsError(UserError):
    message_template = "Not authorized"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class UserNotFoundError(UserError):
    message_template = "User with id {user_id} not found"

    def __init__(self, user_id: UserId) -> None:
        super().__init__(self.message_template.format(user_id=user_id))
