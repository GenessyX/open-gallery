from abc import ABC

from open_gallery.publications.entities import Publication, PublicationId
from open_gallery.shared.repository import Repository


class PublicationRepository(Repository[PublicationId, Publication], ABC): ...
