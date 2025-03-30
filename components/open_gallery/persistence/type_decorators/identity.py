from open_gallery.identity.entities import UserRole
from open_gallery.persistence.type_decorators.enum import StrEnumTypeImpl


class UserRoleTypeImpl(StrEnumTypeImpl[UserRole]):
    target = UserRole
    cache_ok = True
