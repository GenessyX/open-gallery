from abc import ABC

from open_gallery.identity.entities import User, UserId
from open_gallery.shared.repository import Repository


class UserRepository(Repository[UserId, User], ABC): ...
