from open_gallery.shared.exceptions import DomainError


class JWTError(DomainError): ...


class TokenDecodeError(JWTError):
    message_template = "Failed to decode JWT"

    def __init__(self) -> None:
        super().__init__(self.message_template)


class ExpiredTokenError(JWTError):
    message_template = "Token has expired"

    def __init__(self) -> None:
        super().__init__(self.message_template)
