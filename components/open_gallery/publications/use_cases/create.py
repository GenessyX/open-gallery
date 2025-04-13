from open_gallery.identity.entities import User
from open_gallery.publications.dtos import CreatePublicationDto
from open_gallery.publications.entities import Publication
from open_gallery.publications.exceptions import InvalidImagesInPublicationError
from open_gallery.publications.uow import PublicationsUnitOfWork


class CreatePublicationUsecase:
    def __init__(self, uow: PublicationsUnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, create_dto: CreatePublicationDto, actor: User) -> Publication:
        async with self._uow as uow:
            images = await uow.images.get_many(create_dto.linked_image_ids)
            preview_image = await uow.images.get(create_dto.preview_image_id)

            if not preview_image or len(images) != len(create_dto.linked_image_ids):
                raise InvalidImagesInPublicationError

            references = await uow.publications.get_many(create_dto.reference_publication_ids)
            tags = await uow.tags.get_many(create_dto.tag_ids)

            publication = Publication(
                title=create_dto.title,
                images=images,
                preview=preview_image,
                created_by=actor,
                document=create_dto.document,
                approved_by=None,
                references=references,
                tags=tags,
            )

            await uow.publications.save(publication)

        return publication
