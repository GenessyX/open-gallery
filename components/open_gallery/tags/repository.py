from abc import ABC

from open_gallery.shared.repository import Repository
from open_gallery.tags.entities import Tag, TagId


class TagRepository(Repository[TagId, Tag], ABC): ...
