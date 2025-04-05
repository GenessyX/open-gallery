from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, UploadFile

from open_gallery.identity.entities import User
from open_gallery.images.entities import Image
from open_gallery.images.use_cases.upload import UploadImageUsecase
from open_gallery.routing.logging_route import LoggingRoute
from open_gallery.routing.router import APIRouter
from open_gallery.shared_api.authentication.security import authorized

images_router = APIRouter(prefix="/images", route_class=LoggingRoute)


@images_router.post("/upload")
@inject
async def upload_image_endpoint(
    actor: Annotated[User, Depends(authorized)],
    file: UploadFile,
    upload_image: FromDishka[UploadImageUsecase],
) -> Image:
    return await upload_image(actor=actor, file=file.file)
