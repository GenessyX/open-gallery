from dishka import Provider, Scope, provide

from open_gallery.images.use_cases.upload import UploadImageUsecase


class ImageUsecasesProvider(Provider):
    scope = Scope.REQUEST

    upload = provide(UploadImageUsecase)
