from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Body, Depends

from open_gallery.api.identity.schemas import RegisterRequestSchema
from open_gallery.identity.dtos import TokensPair
from open_gallery.identity.entities import User
from open_gallery.identity.exceptions import UserExistsError, WeakPasswordError
from open_gallery.identity.use_cases.login_user import LoginUserUsecase
from open_gallery.identity.use_cases.register_user import RegisterUserUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared_api.authentication.security import authorized
from open_gallery.shared_api.exceptions import define_possible_errors

identity_router = APIRouter(prefix="/identity", route_class=LoggingRoute)


@identity_router.get("")
async def test() -> str:
    return "hello world"


@identity_router.post(
    "/register",
    responses=define_possible_errors(
        {
            400: [WeakPasswordError],
            409: [UserExistsError],
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
)
@inject
async def login_endpoint(
    request_body: Annotated[RegisterRequestSchema, Body()],
    login: FromDishka[LoginUserUsecase],
) -> TokensPair:
    return await login(email=request_body.email, password=request_body.password)


@identity_router.post("/me")
@inject
async def show_me_endpoint(user: Annotated[User, Depends(authorized)]) -> User:
    return user
