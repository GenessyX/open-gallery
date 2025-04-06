from dishka import Provider, Scope, provide

from open_gallery.publications.use_cases.add_comment import AddPublicationCommentUsecase
from open_gallery.publications.use_cases.approve import ApprovePublicationUsecase
from open_gallery.publications.use_cases.create import CreatePublicationUsecase
from open_gallery.publications.use_cases.get import GetPublicationUsecase
from open_gallery.publications.use_cases.get_list import GetPublicationsListUsecase
from open_gallery.publications.use_cases.get_not_approved import GetNotApprovedPublicationsUsecase
from open_gallery.publications.use_cases.react import ReactToPublicationUsecase


class PublicationUsecasesProvider(Provider):
    scope = Scope.REQUEST

    get = provide(GetPublicationUsecase)
    create = provide(CreatePublicationUsecase)
    add_comment = provide(AddPublicationCommentUsecase)
    react = provide(ReactToPublicationUsecase)
    get_list = provide(GetPublicationsListUsecase)
    approve = provide(ApprovePublicationUsecase)
    get_not_approved = provide(GetNotApprovedPublicationsUsecase)
