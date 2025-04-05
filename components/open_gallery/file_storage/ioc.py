from dishka import Provider, Scope, provide

from open_gallery.file_storage.impl.s3.storage import S3FileStorage
from open_gallery.file_storage.interface import FileStorage


class FileStorageProvider(Provider):
    scope = Scope.APP

    storage = provide(S3FileStorage, provides=FileStorage)
