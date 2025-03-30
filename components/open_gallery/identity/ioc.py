from dishka import Provider, Scope, provide

from open_gallery.identity.use_cases.register_user import RegisterUserUsecase


class IdentityUsecasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUserUsecase)
