import webbrowser

from typing import Union
from secrets import token_urlsafe
from urllib.parse import urlparse, parse_qs

from .token import Token
from .expiring import Credentials
from .refreshing import RefreshingToken, RefreshingCredentials


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
        raise KeyError(f'Parameter `{param}` not available!')
    elif len(code) > 1:
        raise KeyError(f'Multiple values for `{param}`!')

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
    return _parse_url_param(url, 'code')


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
    return _parse_url_param(url, 'state')


class UserAuth:
    """
    Implement user authorisation flow.

    Implements all steps and security checks for user authorisation.
    The responsibility of the caller is to redirect a user to the given URL
    and provide the resulting redirect URI or its parameters.

    Parameters
    ----------
    cred
        credentials client
    scope
        token privileges, accepts a :class:`Scope`, a single :class:`scope`,
        a list of :class:`scopes <scope>` and strings for :class:`Scope`,
        or a space-separated list of scopes as a string

    Attributes
    ----------
    url: str
        address to redirect a user to for authorisation
    state: str
        generated additional state

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
    """

    def __init__(self, cred: Union[Credentials, RefreshingCredentials], scope=None):
        self._cred = cred
        self.state = gen_state()
        self.url = self._cred.user_authorisation_url(
            scope, self.state, show_dialog=True
        )

    def __repr__(self):
        options = [
            f'cred={self._cred!r}',
            f'url={self.url!r}',
            f'state={self.state!r}',
        ]
        return type(self).__name__ + '(' + ', '.join(options) + ')'

    def request_token(
        self,
        code: str = None,
        state: str = None,
        url: str = None,
    ) -> Union[Token, RefreshingToken]:
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
        Union[Token, RefreshingToken]
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
            raise AssertionError(
                f'Inconsistent state! Expected `{self.state}`, got `{state}`.'
            )

        return self._cred.request_user_token(code)


def request_client_token(
    client_id: str,
    client_secret: str
) -> RefreshingToken:
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
    scope=None
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

    print('Opening browser for Spotify login...')
    webbrowser.open(auth.url)
    redirected = input('Please paste redirect URL: ').strip()
    return auth.request_token(url=redirected)


def refresh_user_token(
    client_id: str,
    client_secret: str,
    refresh_token: str
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
