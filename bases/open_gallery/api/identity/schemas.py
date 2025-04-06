from open_gallery.identity.entities import UserRole
from open_gallery.jwt.interface import SerializedToken
from open_gallery.shared.types import Email, SecretValue
from open_gallery.shared_api.model import APIModel


class RegisterRequestSchema(APIModel):
    email: Email
    password: SecretValue[str]


class RefreshTokenRequestSchema(APIModel):
    refresh_token: SecretValue[SerializedToken]


class SetUserRoleRequestSchema(APIModel):
    role: UserRole
