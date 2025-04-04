from dishka import FromDishka, Provider, Scope, provide
from fastapi import Request

from open_gallery.identity.dtos import AccessTokenPayload
from open_gallery.identity.entities import User, UserId, UserRole
from open_gallery.identity.exceptions import AuthorizationError
from open_gallery.identity.repository import UserRepository
from open_gallery.jwt.interface import JWTService
from open_gallery.shared.entity import EntityId
from open_gallery.shared_api.authentication.security import security


class AuthorizationProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    async def access_token(
        self,
        request: Request,
        jwt_service: FromDishka[JWTService[AccessTokenPayload]],
    ) -> AccessTokenPayload:
        credentials = await security(request)
        if not credentials:
            raise AuthorizationError
        return jwt_service.decode(credentials.credentials)

    @provide(scope=Scope.REQUEST)
    async def user_role(self, access_token: FromDishka[AccessTokenPayload]) -> UserRole:
        return access_token.role

    @provide(scope=Scope.REQUEST)
    async def user(
        self,
        request: Request,
        jwt_service: FromDishka[JWTService[AccessTokenPayload]],
        user_repository: FromDishka[UserRepository],
    ) -> User:
        credentials = await security(request)
        if not credentials:
            raise AuthorizationError
        decoded_token = jwt_service.decode(credentials.credentials)
        user = await user_repository.get(entity_id=UserId(EntityId(decoded_token.sub)))
        if not user:
            raise AuthorizationError
        return user
