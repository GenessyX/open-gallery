from open_gallery.shared.types import Email, SecretValue
from open_gallery.shared_api.model import APIModel


class RegisterRequestSchema(APIModel):
    email: Email
    password: SecretValue[str]
