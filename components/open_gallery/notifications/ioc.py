from dishka import Provider, Scope, provide

from open_gallery.notifications.use_cases.get_notifications import GetUserNotificationsUsecase


class NotificationUsecasesProvider(Provider):
    scope = Scope.REQUEST

    get = provide(GetUserNotificationsUsecase)
