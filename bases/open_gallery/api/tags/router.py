from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Body

from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared_api.model import APIModel
from open_gallery.tags.dtos import CreateTagDto
from open_gallery.tags.entities import Tag
from open_gallery.tags.use_cases.create import CreateTagUsecase

tags_router = APIRouter(
    prefix="/tags",
    route_class=LoggingRoute,
    tags=["Tags"],
)


class Schema(CreateTagDto, APIModel): ...


@tags_router.post("")
@inject
async def create_tag_endpoint(
    create_dto: Annotated[CreateTagDto, Body()],
    create_tag: FromDishka[CreateTagUsecase],
) -> Tag:
    return await create_tag(create_dto)
