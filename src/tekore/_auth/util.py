from __future__ import annotations

import webbrowser
from secrets import token_urlsafe
from urllib.parse import parse_qs, urlparse

from .expiring import Credentials, Token
from .refreshing import RefreshingCredentials, RefreshingToken


def gen_state(n_bytes: int = 32) -> str:
    """
    Generate state to use in user authorisation.

    The generated state is random and URL-safe.
    It is generated using :func:`secrets.token_urlsafe`.
    """
    return token_urlsafe(n_bytes)


def _parse_url_param(url: str, param: str) -> str:
    query = urlparse(url).query
    code = parse_qs(query).get(param, None)

    if code is None:
        msg = f"Passed URL contains no parameter `{param}`!"
        raise KeyError(msg)
    if len(code) > 1:
        msg = f"Passed URL contains multiple values for `{param}`!"
        raise KeyError(msg)

    return code[0]


def parse_code_from_url(url: str) -> str:
    """
    Parse an URL for parameter 'code'.

    Returns
    -------
    str
        value of 'code'

    Raises
    ------
    KeyError
        if 'code' is not available or has multiple values
    """
    return _parse_url_param(url, "code")


def parse_state_from_url(url: str) -> str:
    """
    Parse an URL for parameter 'state'.

    Returns
    -------
    str
        value of 'state'

    Raises
    ------
    KeyError
        if 'state' is not available or has multiple values
    """
    return _parse_url_param(url, "state")


class UserAuth:
    """
    Implement user authorisation flow.

    Implements all steps and security checks for user authorisation.
    The responsibility of the caller is to redirect a user to the given URL
    and provide the resulting redirect URI or its parameters.
    Can be used with an asynchronous credentials client.

    Parameters
    ----------
    cred
        credentials client
    scope
        token privileges, accepts a :class:`Scope`, a single :class:`scope`,
        a list of :class:`scopes <scope>` and strings for :class:`Scope`,
        or a space-separated list of scopes as a string
    pkce
        use proof key for code exchange

    Attributes
    ----------
    url: str
        address to redirect a user to for authorisation
    state: str
        generated additional state
    verifier: str
        PKCE code verifier, :class:`None` if PKCE is not used

    Examples
    --------
    .. code:: python

        auth = tk.UserAuth(cred, scope)

        # Redirect user to auth.url and parse parameters
        code, state = ...
        token = auth.request_token(code, state)

        # Or leave parsing to UserAuth
        redirected = ...
        token = auth.request_token(url=redirected)

        # With an asynchronous client
        token = await auth.request_token(url=redirected)
    """

    def __init__(
        self, cred: Credentials | RefreshingCredentials, scope=None, pkce: bool = False
    ) -> None:
        self._cred = cred
        self.state = gen_state()
        self.verifier = None
        if pkce:
            self.url, self.verifier = self._cred.pkce_user_authorisation(
                scope, self.state
            )
        else:
            self.url = self._cred.user_authorisation_url(
                scope, self.state, show_dialog=True
            )

    def __repr__(self) -> str:
        options = [
            f"cred={self._cred!r}",
            f"url={self.url!r}",
            f"state={self.state!r}",
            f"verifier={self.verifier}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    def request_token(
        self, code: str | None = None, state: str | None = None, url: str | None = None
    ) -> Token | RefreshingToken:
        """
        Verify state consistency and request token.

        Parameters
        ----------
        code
            code from redirect parameters, required if url was not specified
        state
            state from redirect parameters, required if url was not specified
        url
            if specified, code and state are parsed from this URL instead

        Returns
        -------
        Token | RefreshingToken
            access token

        Raises
        ------
        AssertionError
            if state is inconsistent
        """
        if url is not None:
            code = parse_code_from_url(url)
            state = parse_state_from_url(url)

        if self.state != state:
            msg = f"Inconsistent state! Expected `{self.state}`, got `{state}`."
            raise AssertionError(msg)

        if self.verifier is not None:
            return self._cred.request_pkce_token(code, self.verifier)
        return self._cred.request_user_token(code)


def request_client_token(client_id: str, client_secret: str) -> RefreshingToken:
    """
    Request for client credentials.

    Parameters
    ----------
    client_id
        client ID
    client_secret
        client secret

    Returns
    -------
    RefreshingToken
        automatically refreshing client token
    """
    cred = RefreshingCredentials(client_id, client_secret)
    return cred.request_client_token()


def prompt_for_user_token(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    scope=None,
    open_browser: bool = True,
) -> RefreshingToken:
    """
    Prompt for manual authorisation.

    Open a web browser for the user to log in with Spotify.
    Prompt to paste the URL after logging in to complete authorisation.

    Parameters
    ----------
    client_id
        client ID
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    scope
        token privileges, accepts a :class:`Scope`, a single :class:`scope`,
        a list of :class:`scopes <scope>` and strings for :class:`Scope`,
        or a space-separated list of scopes as a string
    open_browser
        open a web browser with auth url, or just print it

    Returns
    -------
    RefreshingToken
        automatically refreshing user token

    Raises
    ------
    AssertionError
        if state is inconsistent
    """
    cred = RefreshingCredentials(client_id, client_secret, redirect_uri)
    auth = UserAuth(cred, scope=scope)

    if open_browser:
        print("Opening browser for Spotify login...")  # noqa: T201
        webbrowser.open(auth.url)
    else:
        print("Open this URL in your browser: " + auth.url)  # noqa: T201
    redirected = input("Paste the final redirected URL from the browser: ").strip()
    return auth.request_token(url=redirected)


def refresh_user_token(
    client_id: str, client_secret: str, refresh_token: str
) -> RefreshingToken:
    """
    Request a refreshed user token.

    Parameters
    ----------
    client_id
        client ID
    client_secret
        client secret
    refresh_token
        refresh token

    Returns
    -------
    RefreshingToken
        automatically refreshing user token
    """
    cred = RefreshingCredentials(client_id, client_secret)
    return cred.refresh_user_token(refresh_token)


def prompt_for_pkce_token(
    client_id: str, redirect_uri: str, scope=None, open_browser: bool = True
) -> RefreshingToken:
    """
    Prompt for manual authorisation with PKCE.

    Open a web browser for the user to log in with Spotify.
    Prompt to paste the URL after logging in to complete authorisation.

    Parameters
    ----------
    client_id
        client ID
    redirect_uri
        whitelisted redirect URI
    scope
        token privileges, accepts a :class:`Scope`, a single :class:`scope`,
        a list of :class:`scopes <scope>` and strings for :class:`Scope`,
        or a space-separated list of scopes as a string
    open_browser
        open a web browser with auth url, or just print it

    Returns
    -------
    RefreshingToken
        automatically refreshing PKCE user token

    Raises
    ------
    AssertionError
        if state is inconsistent
    """
    cred = RefreshingCredentials(client_id, redirect_uri=redirect_uri)
    auth = UserAuth(cred, scope=scope, pkce=True)

    if open_browser:
        print("Opening browser for Spotify login...")  # noqa: T201
        webbrowser.open(auth.url)
    else:
        print("Open this URL in your browser: " + auth.url)  # noqa: T201
    redirected = input("Paste the final redirected URL from the browser: ").strip()
    return auth.request_token(url=redirected)


def refresh_pkce_token(client_id: str, refresh_token: str) -> RefreshingToken:
    """
    Request a refreshed PKCE user token.

    Parameters
    ----------
    client_id
        client ID
    refresh_token
        refresh token

    Returns
    -------
    RefreshingToken
        automatically refreshing user token
    """
    cred = RefreshingCredentials(client_id)
    return cred.refresh_pkce_token(refresh_token)
