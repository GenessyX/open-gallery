from typing import override

from open_gallery.shared.use_case import Usecase
from open_gallery.tags.dtos import CreateTagDto
from open_gallery.tags.entities import Tag
from open_gallery.tags.exceptions import TagNotFoundError
from open_gallery.tags.uow import TagsUnitOfWork


class CreateTagUsecase(Usecase):
    def __init__(self, uow: TagsUnitOfWork) -> None:
        self._uow = uow

    @override
    async def __call__(self, create_dto: CreateTagDto) -> Tag:
        async with self._uow as uow:
            tag = create_dto.convert_to_tag()

            if create_dto.parent_id:
                root = await uow.tags.get(create_dto.parent_id)
                if not root:
                    raise TagNotFoundError(create_dto.parent_id)
                root.children.append(tag)
                await uow.tags.save(root)
            else:
                await uow.tags.save(tag)

        return tag
