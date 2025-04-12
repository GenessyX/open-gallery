from dishka import FromDishka, Provider, Scope, provide
from fastapi import Request
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient_to_detached

from open_gallery.identity.dtos import AccessTokenPayload
from open_gallery.identity.entities import User, UserId, UserRole
from open_gallery.identity.exceptions import AuthorizationError
from open_gallery.jwt.interface import JWTService
from open_gallery.shared.entity import EntityId
from open_gallery.shared.types import SecretValue
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
        session: FromDishka[AsyncSession],
    ) -> User:
        credentials = await security(request)
        if not credentials:
            raise AuthorizationError
        decoded_token = jwt_service.decode(credentials.credentials)

        user = User(
            id=UserId(EntityId(decoded_token.sub)),
            email=decoded_token.email,
            password=SecretValue(""),
            role=decoded_token.role,
            verified=decoded_token.verified,
        )

        make_transient_to_detached(user)
        await session.merge(user, load=False)

        session.identity_map.add(inspect(user))  # type: ignore[arg-type]

        return user
