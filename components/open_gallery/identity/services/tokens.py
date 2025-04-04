from open_gallery.identity.dtos import AccessTokenPayload, RefreshTokenPayload, TokensPair
from open_gallery.identity.entities import User
from open_gallery.identity.settings import TokensSettings
from open_gallery.jwt.interface import JWTService


class TokensService:
    def __init__(
        self,
        access_token_jwt_service: JWTService[AccessTokenPayload],
        refresh_token_jwt_service: JWTService[RefreshTokenPayload],
        settings: TokensSettings,
    ) -> None:
        self._access_token_jwt_service = access_token_jwt_service
        self._refresh_token_jwt_service = refresh_token_jwt_service
        self._settings = settings

    def generate_tokens(self, user: User) -> TokensPair:
        access_token = self._access_token_jwt_service.encode(
            payload=AccessTokenPayload(
                sub=str(user.id),
                role=user.role,
            ),
            expires_in=self._settings.access_token_ttl,
        )
        refresh_token = self._refresh_token_jwt_service.encode(
            payload=RefreshTokenPayload(
                sub=str(user.id),
            ),
            expires_in=self._settings.refresh_token_ttl,
        )
        return TokensPair(access_token=access_token, refresh_token=refresh_token)
