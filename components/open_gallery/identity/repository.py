from open_gallery.identity.entities import User, UserId
from open_gallery.shared.repository import Repository

type UserRepository = Repository[UserId, User]
