from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi.security import HTTPBearer

from open_gallery.identity.entities import User, UserRole

security = HTTPBearer()


@inject
async def authorized(
    user: FromDishka[User],
) -> User:
    return user


@inject
async def user_role(
    user_role: FromDishka[UserRole],
) -> UserRole:
    return user_role
