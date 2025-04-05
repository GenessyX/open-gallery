from http import HTTPStatus
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Body, Depends, Query

from open_gallery.api.identity.schemas import RefreshTokenRequestSchema, RegisterRequestSchema
from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.entities import User
from open_gallery.identity.exceptions import (
    InvalidCredentialsError,
    UserExistsError,
    WeakPasswordError,
)
from open_gallery.identity.use_cases.login_user import LoginUserUsecase
from open_gallery.identity.use_cases.refresh_token import RefreshTokenUsecase
from open_gallery.identity.use_cases.register_user import RegisterUserUsecase
from open_gallery.identity.use_cases.verify_user import VerifyUserUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared_api.authentication.security import authorized
from open_gallery.shared_api.exceptions import authorization_errors, define_possible_errors

identity_router = APIRouter(prefix="/identity", route_class=LoggingRoute)


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
    request_body: Annotated[RegisterRequestSchema, Body()],
    login: FromDishka[LoginUserUsecase],
) -> TokensPair:
    return await login(email=request_body.email, password=request_body.password)


@identity_router.get(
    "/me",
    responses=define_possible_errors(
        authorization_errors(),
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
    request_body: Annotated[RefreshTokenRequestSchema, Body()],
    refresh: FromDishka[RefreshTokenUsecase],
) -> TokensPair:
    return await refresh(request_body.refresh_token)
