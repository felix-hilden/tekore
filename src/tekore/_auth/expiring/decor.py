from collections.abc import Callable

from httpx import codes

from tekore._sender import Request, Response
from tekore._sender.error import RefreshTokenInvalid, get_error

from .token import Token


def handle_errors(request: Request, response: Response) -> None:
    """Examine response and raise errors accordingly."""
    if not codes.is_error(response.status_code):
        return

    error_cls = get_error(response.status_code)
    if codes.is_client_error(response.status_code):
        error = response.content["error"]
        error_str = f"{response.status_code} {error}"
        description = response.content.get("error_description", None)
        if description is not None:
            error_str += ": " + description
        if error == "invalid_grant":
            error_cls = RefreshTokenInvalid
    else:
        error_str = "Unexpected error!"

    raise error_cls(error_str, request=request, response=response)


def parse_token(uses_pkce: bool) -> Callable:
    """Wrap token parsing conditional to PKCE usage."""

    def func(request: Request, response: Response) -> Token:
        """Parse token object from response."""
        handle_errors(request, response)
        return Token(response.content, uses_pkce)

    return func


def parse_refreshed_token(uses_pkce: bool) -> Callable:
    """Wrap token parsing conditional to PKCE usage."""

    def func(request: Request, response: Response, refresh_token: str) -> Token:
        """Replace new refresh token with old value if empty."""
        handle_errors(request, response)
        refreshed = Token(response.content, uses_pkce)

        if refreshed.refresh_token is None:
            refreshed._refresh_token = refresh_token

        return refreshed

    return func
