from fastapi import Response

from open_gallery.identity.dtos import TokensPair


def set_auth_cookies(response: Response, tokens: TokensPair) -> None:
    response.set_cookie("access-token", tokens.access_token)
    response.set_cookie("refresh-token", tokens.refresh_token, path="/api/v1/identity")


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access-token")
    response.delete_cookie("refresh-token", path="/api/v1/identity")
