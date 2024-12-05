from __future__ import annotations

from tekore._sender import Sender

from .expiring import AccessToken, Credentials, Token
from .scope import Scope


class RefreshingToken(AccessToken):
    """
    Automatically refreshing access token.

    Returned from utility functions and :class:`RefreshingCredentials`.
    It shouldn't have to be instantiated outside of the functions,
    unless you are sure that you want to.

    Uses an instance of :class:`Credentials` to automatically request
    a new access token when the old one is about to expire.
    This occurs when the :attr:`access_token` property is read.

    Both :attr:`expires_in` and :attr:`expires_at` are always ``None``,
    and :attr:`is_expiring` is always ``False``.

    Parameters
    ----------
    token
        access token object
    credentials
        credentials manager for token refreshing

    Attributes
    ----------
    credentials
        credentials manager for token refreshing
    """

    def __init__(self, token: Token, credentials: Credentials) -> None:
        self._token = token
        self.credentials = credentials

    def __repr__(self) -> str:
        options = [
            f"access_token={self.access_token!r}",
            f"refresh_token={self.refresh_token!r}",
            f"scope={self.scope!r}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    @property
    def access_token(self) -> str:
        """Bearer token value."""
        if self._token.is_expiring:
            self._token = self.credentials.refresh(self._token)

        return self._token.access_token

    @property
    def refresh_token(self) -> str | None:
        """
        Refresh token for generating new access tokens.

        ``None`` if the token is an application token.
        """
        return self._token.refresh_token

    @property
    def token_type(self) -> str:
        """How the token may be used, always 'Bearer'."""
        return self._token.token_type

    @property
    def scope(self) -> Scope:
        """
        Privileges granted to the token.

        Empty :class:`Scope` if the token is an application token
        or a user token without any scopes.
        """
        return self._token.scope

    @property
    def expires_in(self) -> None:
        """Seconds until token expiration, always ``None``."""
        return None

    @property
    def expires_at(self) -> None:
        """When the token expires, always ``None``."""
        return None

    @property
    def is_expiring(self) -> bool:
        """Determine whether token is about to expire, always ``False``."""
        return False

    @property
    def uses_pkce(self) -> bool:
        """Proof key for code exchange used in authorisation."""
        return self._token.uses_pkce


class RefreshingCredentials:
    """
    Synchronous client for self-refreshing tokens.

    Delegates to an underlying :class:`Credentials` manager
    and parses tokens it returns into :class:`RefreshingToken`.

    Parameters
    ----------
    client_id
        client id
    client_secret
        client secret, not required for PKCE user authorisation
    redirect_uri
        whitelisted redirect URI, required for user authorisation
    sender
        synchronous request sender

    Attributes
    ----------
    credentials
        underlying credentials manager for token refreshing
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
        sender: Sender | None = None,
    ) -> None:
        self.credentials = Credentials(
            client_id, client_secret, redirect_uri, sender, asynchronous=False
        )

    def __repr__(self) -> str:
        options = [
            f"client_id={self.credentials.client_id!r}",
            f"client_secret={self.credentials.client_secret!r}",
            f"redirect_uri={self.credentials.redirect_uri!r}",
            f"sender={self.credentials.sender!r}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    def request_client_token(self) -> RefreshingToken:
        """
        Request a refreshing client token.

        Returns
        -------
        RefreshingToken
            automatically refreshing client token
        """
        token = self.credentials.request_client_token()
        return RefreshingToken(token, self.credentials)

    def user_authorisation_url(
        self, scope=None, state: str | None = None, show_dialog: bool = False
    ) -> str:
        """
        Construct an authorisation URL.

        Step 1/2 in authorisation code flow.
        User should be redirected to the resulting URL for authorisation.
        Step 2/2: :meth:`request_user_token`.

        Parameters
        ----------
        scope
            token privileges, accepts a :class:`Scope`, a single :class:`scope`,
            a list of :class:`scopes <scope>` and strings for :class:`Scope`,
            or a space-separated list of scopes as a string
        state
            additional state
        show_dialog
            force login dialog even if previously authorised

        Returns
        -------
        str
            login URL
        """
        return self.credentials.user_authorisation_url(scope, state, show_dialog)

    def request_user_token(self, code: str) -> RefreshingToken:
        """
        Request a new refreshing user token.

        Step 2/2 in authorisation code flow.
        Code is provided as a URL parameter in the redirect URI
        after login in step 1: :meth:`user_authorisation_url`.

        Parameters
        ----------
        code
            code from redirect parameters

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self.credentials.request_user_token(code)
        return RefreshingToken(token, self.credentials)

    def refresh_user_token(self, refresh_token: str) -> RefreshingToken:
        """
        Request an automatically refreshing user token with a refresh token.

        Parameters
        ----------
        refresh_token
            refresh token

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self.credentials.refresh_user_token(refresh_token)
        return RefreshingToken(token, self.credentials)

    def pkce_user_authorisation(
        self, scope=None, state: str | None = None, verifier_bytes: int = 32
    ) -> tuple[str, str]:
        """
        Construct authorisation URL and verifier.

        Step 1/2 in authorisation code flow with proof key for code exchange.
        The user should be redirected to the resulting URL for authorisation.
        The verifier is passed to :meth:`request_pkce_token` in step 2.

        Parameters
        ----------
        scope
            token privileges, accepts a :class:`Scope`, a single :class:`scope`,
            a list of :class:`scopes <scope>` and strings for :class:`Scope`,
            or a space-separated list of scopes as a string
        state
            additional state
        verifier_bytes
            number of bytes to generate PKCE verifier with, ``32 <= bytes <= 96``.
            The specified range of bytes generates the appropriate number of
            characters (43 - 128) after base-64 encoding, as required in RFC 7636.

        Returns
        -------
        tuple[str, str]
            authorisation URL and PKCE code verifier
        """
        return self.credentials.pkce_user_authorisation(scope, state, verifier_bytes)

    def request_pkce_token(self, code: str, verifier: str) -> RefreshingToken:
        """
        Request a new PKCE user token.

        Step 2/2 in authorisation code flow with proof key for code exchange.
        Code is provided as a URL parameter in the redirect URI
        after login in step 1: :meth:`pkce_user_authorisation`.

        Parameters
        ----------
        code
            code from redirect parameters
        verifier
            PKCE code verifier generated for authorisation URL

        Returns
        -------
        RefreshingToken
            user access token
        """
        token = self.credentials.request_pkce_token(code, verifier)
        return RefreshingToken(token, self.credentials)

    def refresh_pkce_token(self, refresh_token: str) -> RefreshingToken:
        """
        Request a refreshed PKCE user token.

        Parameters
        ----------
        refresh_token
            refresh token

        Returns
        -------
        RefreshingToken
            refreshed user access token
        """
        token = self.credentials.refresh_pkce_token(refresh_token)
        return RefreshingToken(token, self.credentials)
