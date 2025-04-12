from open_gallery.notifications.entities import NotificationType
from open_gallery.persistence.type_decorators.enum import StrEnumTypeImpl


class NotificationTypeTypeImpl(StrEnumTypeImpl[NotificationType]):
    target = NotificationType
    cache_ok = True
