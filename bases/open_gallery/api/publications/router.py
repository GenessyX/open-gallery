from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Body, Depends, Path

from open_gallery.identity.entities import User
from open_gallery.publications.dtos import CreatePublicationDto
from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.publications.use_cases.create import CreatePublicationUsecase
from open_gallery.publications.use_cases.get import GetPublicationUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared_api.authentication.security import authorized

publications_router = APIRouter(
    prefix="/publications",
    route_class=LoggingRoute,
    tags=["Publications"],
)


@publications_router.get("/{publication_id}")
@inject
async def get_publciation_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    actor: Annotated[User, Depends(authorized)],
    get_publication: FromDishka[GetPublicationUsecase],
) -> Publication:
    return await get_publication(publication_id, actor)


@publications_router.post("")
@inject
async def create_publication_endpoint(
    create_dto: Annotated[CreatePublicationDto, Body()],
    actor: Annotated[User, Depends(authorized)],
    create_publication: FromDishka[CreatePublicationUsecase],
) -> Publication:
    return await create_publication(create_dto, actor)
