from dishka import Provider, Scope, provide

from open_gallery.tags.use_cases.create import CreateTagUsecase


class TagUsecasesProvider(Provider):
    scope = Scope.REQUEST

    create = provide(CreateTagUsecase)
