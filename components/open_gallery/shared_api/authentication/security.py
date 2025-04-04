from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from open_gallery.identity.entities import User, UserRole

security = HTTPBearer()


@inject
async def authorized(
    _: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: FromDishka[User],
) -> User:
    return user


@inject
async def user_role(
    _: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_role: FromDishka[UserRole],
) -> UserRole:
    return user_role
