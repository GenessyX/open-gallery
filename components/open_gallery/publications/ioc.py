from dishka import Provider, Scope, provide

from open_gallery.publications.use_cases.add_comment import AddPublicationCommentUsecase
from open_gallery.publications.use_cases.create import CreatePublicationUsecase
from open_gallery.publications.use_cases.get import GetPublicationUsecase
from open_gallery.publications.use_cases.react import ReactToPublicationUsecase


class PublicationUsecasesProvider(Provider):
    scope = Scope.REQUEST

    get = provide(GetPublicationUsecase)
    create = provide(CreatePublicationUsecase)
    add_comment = provide(AddPublicationCommentUsecase)
    react = provide(ReactToPublicationUsecase)
