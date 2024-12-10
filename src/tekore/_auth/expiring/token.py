from __future__ import annotations

import time
from abc import ABC, abstractmethod

from tekore._auth.scope import Scope


class AccessToken(ABC):
    """Access token base class."""

    @property
    @abstractmethod
    def access_token(self) -> str:
        """
        Bearer token value.

        Used as the string representation of the instance.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Bearer token value."""
        return self.access_token


class Token(AccessToken):
    """
    Expiring access token.

    Represents both client and user tokens.
    The refresh token of a client token is ``None``.
    """

    def __init__(self, token_info: dict, uses_pkce: bool) -> None:
        self._access_token = token_info["access_token"]
        self._token_type = token_info["token_type"]

        scope = token_info.get("scope", "")
        components = scope.split(" ")
        if components[0] == "":
            components = []
        self._scope = Scope(*components)

        self._refresh_token = token_info.get("refresh_token")
        self._expires_at = int(time.time()) + token_info["expires_in"]
        self._uses_pkce = uses_pkce

    def __repr__(self) -> str:
        options = [
            f"access_token={self.access_token!r}",
            f"refresh_token={self.refresh_token!r}",
            f"expires_at={self.expires_at!r}",
            f"scope={self.scope!r}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    @property
    def access_token(self) -> str:
        """Bearer token value."""
        return self._access_token

    @property
    def refresh_token(self) -> str | None:
        """
        Refresh token for generating new access tokens.

        ``None`` if the token is an application token.
        """
        return self._refresh_token

    @property
    def token_type(self) -> str:
        """How the token may be used, always 'Bearer'."""
        return self._token_type

    @property
    def scope(self) -> Scope:
        """
        Privileges granted to the token.

        Empty :class:`Scope` if the token is an application token
        or a user token without any scopes.
        """
        return self._scope

    @property
    def expires_in(self) -> int:
        """Seconds until token expiration."""
        return self.expires_at - int(time.time())

    @property
    def expires_at(self) -> int:
        """When the token expires."""
        return self._expires_at

    @property
    def is_expiring(self) -> bool:
        """Determine whether token is about to expire."""
        return self.expires_in < 60  # noqa: PLR2004

    @property
    def uses_pkce(self) -> bool:
        """Proof key for code exchange used in authorisation."""
        return self._uses_pkce
