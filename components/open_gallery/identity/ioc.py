from dishka import Provider, Scope, provide

from open_gallery.dishka.providers.settings import BaseSettingsProvider
from open_gallery.identity.dtos import AccessTokenPayload, RefreshTokenPayload
from open_gallery.identity.services.tokens import TokensService
from open_gallery.identity.services.verification import VerificationService
from open_gallery.identity.settings import IdentitySettings, JWTSettings
from open_gallery.identity.use_cases.get_user_list import GetUsersListUsecase
from open_gallery.identity.use_cases.login_user import LoginUserUsecase
from open_gallery.identity.use_cases.logout_user import LogoutUserUsecase
from open_gallery.identity.use_cases.refresh_token import RefreshTokenUsecase
from open_gallery.identity.use_cases.register_user import RegisterUserUsecase
from open_gallery.identity.use_cases.search_users import SearchUsersUsecase
from open_gallery.identity.use_cases.set_role import SetUserRoleUsecase
from open_gallery.identity.use_cases.verify_user import VerifyUserUsecase
from open_gallery.jwt.impl import JwcryptoJWTService
from open_gallery.jwt.interface import JWTService


class IdentitySettingsProvider(BaseSettingsProvider):
    root_settings = IdentitySettings
    base = False


class IdentityModuleProvider(Provider):
    scope = Scope.APP

    @provide
    def access_token_jwt_service(self, settings: JWTSettings) -> JWTService[AccessTokenPayload]:
        return JwcryptoJWTService(
            secret=settings.secret.get_secret_value(),
            algorithm=settings.algorithm,
            payload_type=AccessTokenPayload,
        )

    @provide
    def refresh_token_jwt_service(self, settings: JWTSettings) -> JWTService[RefreshTokenPayload]:
        return JwcryptoJWTService(
            secret=settings.secret.get_secret_value(),
            algorithm=settings.algorithm,
            payload_type=RefreshTokenPayload,
        )

    tokens_service = provide(TokensService)
    verification_service = provide(VerificationService)


class IdentityUsecasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUserUsecase)
    login = provide(LoginUserUsecase)
    logout = provide(LogoutUserUsecase)
    verify = provide(VerifyUserUsecase)
    refresh = provide(RefreshTokenUsecase)
    set_role = provide(SetUserRoleUsecase)
    get_list = provide(GetUsersListUsecase)
    search = provide(SearchUsersUsecase)
