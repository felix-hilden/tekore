"""
util
====

Utility module for your convenience <3

The main motivation for this module is to make authorisation effortless.
That goal is achieved by three mechanisms: reading configuration from
environment variables, an automatically refreshing access token and
functions that implement everything needed to retrieve tokens.
The effect is easy configuration, user authorisation and
a strong independent token.

.. code:: python

    from spotipy import util

    conf = util.credentials_from_environment()
    app_token = util.request_client_token(*conf)
    user_token = util.prompt_for_user_token(*conf)

    # Save the refresh token to avoid authenticating again
    refresh_token = ...     # Load refresh token
    user_token = util.request_refreshed_token(*conf, refresh_token)

If you authenticate with a server but would still like to use
:class:`RefreshingToken`, you can use the :class:`RefreshingCredentials`
manager that is used by the functions above to create refreshing tokens.

.. code:: python

    cred = util.RefreshingCredentials(*conf)

    # Client credentials flow
    app_token = cred.request_client_token()

    # Authorisation code flow
    url = cred.user_authorisation_url()
    code = ...  # Redirect user to login and retrieve code
    user_token = cred.request_user_token(code)

    # Reload a token
    user_token = cred.request_refreshed_token(refresh_token)

This module exists solely to make developing applications easier.
Some applications might have different needs,
so please do create your own versions of these routines.
Particularly, ``prompt_for_user_token`` is only suited for local use
as it opens up a web browser for the user to log in with.
"""

import os
import webbrowser

from urllib.parse import urlparse, parse_qs
from spotipy.auth import AccessToken, Token, Credentials


class RefreshingToken(AccessToken):
    """
    Automatically refreshing access token.

    Returned from utility functions and :class:`RefreshingCredentials`.
    It shouldn't have to be instantiated outside of the functions,
    unless you are sure that you want to.

    Uses an instance of :class:`Credentials` to automatically request a new
    access token when the old one is about to expire. This occurs when the
    `access_token` property is read.

    Both ``expires_in`` and ``expires_at`` always return ``None``,
    and ``is_expiring`` is always ``False``.

    Parameters
    ----------
    token
        access token object
    credentials
        credentials manager for token refreshing
    """
    def __init__(self, token: Token, credentials: Credentials):
        self._token = token
        self._credentials = credentials

    @property
    def access_token(self) -> str:
        if self._token.is_expiring():
            if self.refresh_token is None:
                self._token = self._credentials.request_client_token()
            else:
                self._token = self._credentials.refresh(self._token)

        return self._token.access_token

    @property
    def refresh_token(self):
        return self._token.refresh_token

    @property
    def token_type(self):
        return self._token.token_type

    @property
    def scope(self):
        return self._token.scope

    @property
    def expires_in(self) -> None:
        return None

    @property
    def expires_at(self) -> None:
        return None

    @staticmethod
    def is_expiring() -> bool:
        return False


class RefreshingCredentials:
    """
    Client for retrieving automatically refreshing access tokens.

    Delegates to an underlying :class:`Credentials` manager
    and parses tokens it returns to :class:`RefreshingToken`.

    Parameters
    ----------
    client_id
        client id
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    """
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self._client = Credentials(client_id, client_secret, redirect_uri)

    def request_client_token(self) -> RefreshingToken:
        """
        Request for refreshing access token using application credentials.

        Returns
        -------
        RefreshingToken
            automatically refreshing client token
        """
        token = self._client.request_client_token()
        return RefreshingToken(token, self._client)

    def user_authorisation_url(self, scope=None, state: str = None) -> str:
        """
        Construct an authorisation URL for Spotify login.

        Parameters
        ----------
        scope
            access rights as a space-separated list
        state
            additional state

        Returns
        -------
        str
            URL for Spotify login
        """
        return self._client.user_authorisation_url(scope, state)

    def request_user_token(
            self,
            code: str,
            scope=None,
            state: str = None
    ) -> RefreshingToken:
        """
        Request for refreshing access token using a code
        provided by a request from the Spotify server.

        Parameters
        ----------
        code
            code from request parameters
        scope
            access rights as a space-separated list
        state
            additional state

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self._client.request_user_token(code, scope, state)
        return RefreshingToken(token, self._client)

    def request_refreshed_token(self, refresh_token: str) -> RefreshingToken:
        """
        Retrieve a token using a refresh token.

        Parameters
        ----------
        refresh_token
            refresh token

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self._client.request_refreshed_token(refresh_token)
        return RefreshingToken(token, self._client)


def read_environment(*variables: str) -> tuple:
    """
    Read environment variables.

    Parameters
    ----------
    variables
        environment variable names to read

    Returns
    -------
    tuple
        variable values
    """
    return tuple(os.getenv(var, None) for var in variables)


def credentials_from_environment(
        client_id_var: str = 'SPOTIPY_CLIENT_ID',
        client_secret_var: str = 'SPOTIPY_CLIENT_SECRET',
        redirect_uri_var: str = 'SPOTIPY_REDIRECT_URI'
) -> (str, str, str):
    """
    Read environment variables for application credentials.

    Parameters
    ----------
    client_id_var
        name of the variable containing a client ID
    client_secret_var
        name of the variable containing a client secret
    redirect_uri_var
        name of the variable containing a redirect URI

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found
    """
    return read_environment(client_id_var, client_secret_var, redirect_uri_var)


def parse_code_from_url(url: str) -> str:
    """
    Parse an URL for query string parameter 'code'.
    """
    query = urlparse(url).query
    code = parse_qs(query).get('code', None)

    if code is None:
        raise KeyError('Parameter `code` not available!')
    elif len(code) > 1:
        raise KeyError('Multiple values for `code`!')

    return code[0]


def request_client_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str
) -> RefreshingToken:
    """
    Request for client credentials.

    Parameters
    ----------
    client_id
        client ID of a Spotify App
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI

    Returns
    -------
    RefreshingToken
        automatically refreshing client token
    """
    cred = RefreshingCredentials(client_id, client_secret, redirect_uri)
    return cred.request_client_token()


def prompt_for_user_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope=None
) -> RefreshingToken:
    """
    Prompt for manual authentication.

    Open a web browser for the user to log in with Spotify.
    Prompt to paste the URL after logging in to parse the `code` URL parameter.

    Parameters
    ----------
    client_id
        client ID of a Spotify App
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    scope
        access rights as a space-separated list

    Returns
    -------
    RefreshingToken
        automatically refreshing user token
    """
    cred = RefreshingCredentials(client_id, client_secret, redirect_uri)
    url = cred.user_authorisation_url(scope)

    print('Opening browser for Spotify login...')
    webbrowser.open(url)
    redirected = input('Please paste redirect URL: ').strip()
    code = parse_code_from_url(redirected)
    return cred.request_user_token(code, scope)


def request_refreshed_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        refresh_token: str
) -> RefreshingToken:
    """
    Retrieve a token using a refresh token.

    Parameters
    ----------
    client_id
        client ID of a Spotify App
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    refresh_token
        refresh token

    Returns
    -------
    RefreshingToken
        automatically refreshing user token
    """
    cred = RefreshingCredentials(client_id, client_secret, redirect_uri)
    return cred.request_refreshed_token(refresh_token)
