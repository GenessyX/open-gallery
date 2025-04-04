from dishka import Provider, Scope, provide

from open_gallery.hashing.argon import Argon2Hasher
from open_gallery.hashing.interface import Hasher


class HasherProvider(Provider):
    scope = Scope.APP

    hasher = provide(Argon2Hasher, provides=Hasher)
