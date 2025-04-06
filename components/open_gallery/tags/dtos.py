from dataclasses import dataclass, field

from open_gallery.tags.entities import Tag, TagId


@dataclass(kw_only=True)
class CreateTagDto:
    title: str
    parent_id: TagId | None = None
    children: list["CreateTagDto"] = field(default_factory=list)

    def convert_to_tag(self) -> Tag:
        return Tag(
            title=self.title,
            children=[child.convert_to_tag() for child in self.children],
        )
