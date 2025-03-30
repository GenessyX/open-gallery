from dishka import Provider, Scope, provide

from open_gallery.passwords.complexity.impl import LengthBasedVerifier
from open_gallery.passwords.complexity.interface import PasswordComplexityVerifier


class PasswordsProvider(Provider):
    scope = Scope.APP

    @provide
    def verifier(self) -> PasswordComplexityVerifier:
        return LengthBasedVerifier(8)
