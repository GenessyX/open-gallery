from dishka import Provider, Scope, provide

from open_gallery.hashing.argon import Argon2Hasher
from open_gallery.hashing.interface import Hasher, SaltHasher
from open_gallery.hashing.sha256 import Sha256Hasher


class HasherProvider(Provider):
    scope = Scope.APP

    argon_hasher = provide(Argon2Hasher, provides=SaltHasher)
    sha256_hasher = provide(Sha256Hasher, provides=Hasher)
