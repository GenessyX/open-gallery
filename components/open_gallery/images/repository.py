from abc import ABC

from open_gallery.images.entities import Image, ImageId
from open_gallery.shared.repository import Repository


class ImageRepository(Repository[ImageId, Image], ABC): ...
