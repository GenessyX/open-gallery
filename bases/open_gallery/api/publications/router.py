from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Body, Depends, Path, Query

from open_gallery.api.publications.schemas import AddPublicationCommentRequestSchema, ReactToPublicationRequestSchema
from open_gallery.identity.entities import User
from open_gallery.identity.exceptions import AuthorizationError
from open_gallery.publications.dtos import CreatePublicationDto
from open_gallery.publications.entities import Comment, CommentId, Publication, PublicationId
from open_gallery.publications.use_cases.add_comment import AddPublicationCommentUsecase
from open_gallery.publications.use_cases.approve import ApprovePublicationUsecase
from open_gallery.publications.use_cases.create import CreatePublicationUsecase
from open_gallery.publications.use_cases.delete_comment import DeletePublicationCommentUsecase
from open_gallery.publications.use_cases.get import GetPublicationUsecase
from open_gallery.publications.use_cases.get_comments import GetPublicationCommentsUsecase
from open_gallery.publications.use_cases.get_list import GetPublicationsListUsecase
from open_gallery.publications.use_cases.get_not_approved import GetNotApprovedPublicationsUsecase
from open_gallery.publications.use_cases.get_popular import GetPopularPublicationsUsecase
from open_gallery.publications.use_cases.react import ReactToPublicationUsecase
from open_gallery.publications.use_cases.update_comment import UpdatePublicationCommentUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared.pagination import PaginationParams
from open_gallery.shared_api.authentication.security import authorized, optionally_authorized

publications_router = APIRouter(
    prefix="/publications",
    route_class=LoggingRoute,
    tags=["Publications"],
)


@publications_router.get("")
@inject
async def get_publciations_list_endpoint(
    pagination: Annotated[PaginationParams, Depends()],
    actor: Annotated[User | None, Depends(optionally_authorized)],
    get_publications_list: FromDishka[GetPublicationsListUsecase],
    get_not_approved_publications: FromDishka[GetNotApprovedPublicationsUsecase],
    *,
    approved: Annotated[bool, Query()] = True,
) -> list[Publication]:
    if approved:
        return await get_publications_list(pagination.limit, pagination.offset)
    if not actor:
        raise AuthorizationError
    return await get_not_approved_publications(pagination.limit, pagination.offset, actor)


@publications_router.get("/popular")
@inject
async def get_popular_publications_endpoint(
    get_popular_publications: FromDishka[GetPopularPublicationsUsecase],
    limit: Annotated[int, Query()] = 10,
) -> list[Publication]:
    return await get_popular_publications(limit=limit)


@publications_router.get("/{publication_id}")
@inject
async def get_publciation_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    actor: Annotated[User | None, Depends(optionally_authorized)],
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


@publications_router.post("/{publication_id}/comments")
@inject
async def add_publication_comment_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    request_body: Annotated[AddPublicationCommentRequestSchema, Body()],
    actor: Annotated[User, Depends(authorized)],
    add_comment: FromDishka[AddPublicationCommentUsecase],
) -> Comment:
    return await add_comment(
        publication_id,
        request_body.parent_id,
        request_body.text,
        actor,
    )


@publications_router.get("/{publication_id}/comments")
@inject
async def get_publication_comments_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    pagination: Annotated[PaginationParams, Depends()],
    get_comments: FromDishka[GetPublicationCommentsUsecase],
) -> list[Comment]:
    return await get_comments(
        publication_id,
        pagination.limit,
        pagination.offset,
    )


@publications_router.patch("/{publication_id}/comments/{comment_id}")
@inject
async def update_publication_comment_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    comment_id: Annotated[CommentId, Path()],
    request_body: Annotated[AddPublicationCommentRequestSchema, Body()],
    actor: Annotated[User, Depends(authorized)],
    update_comment: FromDishka[UpdatePublicationCommentUsecase],
) -> Comment:
    return await update_comment(
        publication_id,
        comment_id,
        request_body.text,
        actor,
    )


@publications_router.delete("/{publication_id}/comments/{comment_id}")
@inject
async def delete_publication_comment_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    comment_id: Annotated[CommentId, Path()],
    actor: Annotated[User, Depends(authorized)],
    delete_comment: FromDishka[DeletePublicationCommentUsecase],
) -> bool:
    return await delete_comment(publication_id, comment_id, actor)


@publications_router.post("/{publication_id}/reactions")
@inject
async def react_to_publication_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    request_body: Annotated[ReactToPublicationRequestSchema, Body()],
    actor: Annotated[User, Depends(authorized)],
    react_to_publication: FromDishka[ReactToPublicationUsecase],
) -> bool:
    return await react_to_publication(
        publication_id,
        request_body.reaction_type,
        actor,
    )


@publications_router.post("/{publication_id}/approve")
@inject
async def approve_publication_endpoint(
    publication_id: Annotated[PublicationId, Path()],
    actor: Annotated[User, Depends(authorized)],
    approve_publication: FromDishka[ApprovePublicationUsecase],
) -> Publication:
    return await approve_publication(publication_id, actor)
