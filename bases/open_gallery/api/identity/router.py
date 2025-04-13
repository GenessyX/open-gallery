from http import HTTPStatus
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Body, Cookie, Depends, Path, Query, Response

from open_gallery.api.identity.schemas import RegisterRequestSchema, SetUserRoleRequestSchema
from open_gallery.api.identity.utils import clear_auth_cookies, set_auth_cookies
from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.entities import User, UserId
from open_gallery.identity.exceptions import (
    InvalidCredentialsError,
    UserExistsError,
    WeakPasswordError,
)
from open_gallery.identity.use_cases.get_user_list import GetUsersListUsecase
from open_gallery.identity.use_cases.login_user import LoginUserUsecase
from open_gallery.identity.use_cases.logout_user import LogoutUserUsecase
from open_gallery.identity.use_cases.refresh_token import RefreshTokenUsecase
from open_gallery.identity.use_cases.register_user import RegisterUserUsecase
from open_gallery.identity.use_cases.search_users import SearchUsersUsecase
from open_gallery.identity.use_cases.set_role import SetUserRoleUsecase
from open_gallery.identity.use_cases.verify_user import VerifyUserUsecase
from open_gallery.notifications.entities import GenericNotification
from open_gallery.notifications.use_cases.get_notifications import GetUserNotificationsUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared.pagination import PaginationParams
from open_gallery.shared.types import SecretValue
from open_gallery.shared_api.authentication.security import authorized
from open_gallery.shared_api.exceptions import define_possible_errors

identity_router = APIRouter(prefix="/identity", route_class=LoggingRoute, tags=["Identity"])


@identity_router.get("")
async def test() -> str:
    return "hello world"


@identity_router.post(
    "/register",
    responses=define_possible_errors(
        {
            HTTPStatus.BAD_REQUEST: [WeakPasswordError],
            HTTPStatus.CONFLICT: [UserExistsError],
        },
    ),
)
@inject
async def register_endpoint(
    request_body: Annotated[RegisterRequestSchema, Body()],
    register: FromDishka[RegisterUserUsecase],
) -> TokensPair:
    return await register(email=request_body.email, password=request_body.password)


@identity_router.post(
    "/login",
    responses=define_possible_errors(
        {
            HTTPStatus.UNAUTHORIZED: [InvalidCredentialsError],
        },
    ),
)
@inject
async def login_endpoint(
    response: Response,
    request_body: Annotated[RegisterRequestSchema, Body()],
    login: FromDishka[LoginUserUsecase],
) -> None:
    tokens = await login(email=request_body.email, password=request_body.password)
    set_auth_cookies(response, tokens)


@identity_router.get(
    "/me",
    responses=define_possible_errors(
        {},
        authorized=True,
    ),
)
@inject
async def show_me_endpoint(user: Annotated[User, Depends(authorized)]) -> User:
    return user


@identity_router.get(
    "/verify",
    responses=define_possible_errors(
        {
            HTTPStatus.UNAUTHORIZED: [InvalidCredentialsError],
        },
    ),
)
@inject
async def verify_user_endpoint(
    code: Annotated[str, Query()],
    verify: FromDishka[VerifyUserUsecase],
) -> bool:
    return await verify(code=code)


@identity_router.post(
    "/refresh",
    responses=define_possible_errors(
        {
            HTTPStatus.UNAUTHORIZED: [InvalidCredentialsError],
        },
    ),
)
@inject
async def refresh_token_endpoint(
    response: Response,
    refresh: FromDishka[RefreshTokenUsecase],
    refresh_token: Annotated[SecretValue[str], Cookie(alias="refresh-token")] = SecretValue(""),  # noqa: B008
) -> None:
    tokens = await refresh(refresh_token)
    set_auth_cookies(response, tokens)


@identity_router.post("/logout")
@inject
async def logout_user_endpoint(
    response: Response,
    logout_user: FromDishka[LogoutUserUsecase],
    refresh_token: Annotated[SecretValue[str], Cookie(alias="refresh-token")] = SecretValue(""),  # noqa: B008
) -> None:
    await logout_user(refresh_token)
    clear_auth_cookies(response)


@identity_router.get("/notifications")
@inject
async def get_notifications_endpoint(
    pagination: Annotated[PaginationParams, Depends()],
    actor: Annotated[User, Depends(authorized)],
    get_notifications: FromDishka[GetUserNotificationsUsecase],
) -> list[GenericNotification]:
    return await get_notifications(actor, pagination.limit, pagination.offset)


users_router = APIRouter(prefix="/users", route_class=LoggingRoute, tags=["Users"])


@users_router.get("")
@inject
async def get_users_list_endpoint(
    pagination: Annotated[PaginationParams, Depends()],
    actor: Annotated[User, Depends(authorized)],
    get_users_list: FromDishka[GetUsersListUsecase],
) -> list[User]:
    return await get_users_list(pagination.limit, pagination.offset, actor)


@users_router.get("/search")
@inject
async def search_users_endpoint(
    email: Annotated[str, Query()],
    actor: Annotated[User, Depends(authorized)],
    search_users: FromDishka[SearchUsersUsecase],
) -> list[User]:
    return await search_users(email, actor)


@users_router.post("/{user_id}")
@inject
async def set_user_role_endpoint(
    user_id: Annotated[UserId, Path()],
    request_body: Annotated[SetUserRoleRequestSchema, Body()],
    actor: Annotated[User, Depends(authorized)],
    set_role: FromDishka[SetUserRoleUsecase],
) -> User:
    return await set_role(user_id, request_body.role, actor)


identity_router.include_router(users_router)
