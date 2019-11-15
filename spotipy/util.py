"""
util
====

Utility module for your convenience <3

These functions and classes exist to make developing applications easier.
For larger-scale applications they might not be enough, so please do create
versions of these routines that meet your needs.
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

    Uses an instance of a credentials manager to automatically request a new
    access token when the old one is about to expire. This occurs when the
    `access_token` property is read.

    Parameters
    ----------
    token
        access token object
    credentials
        credentials manager for token refreshing
    """
    def __init__(self, token: Token, credentials: Credentials):
        self._token = token
        self.credentials = credentials

    @property
    def access_token(self) -> str:
        if self._token.is_expiring():
            self._token = self.credentials.refresh(self._token)

        return self._token.access_token

    @property
    def token_type(self):
        return self._token.token_type

    @property
    def scope(self):
        return self._token.scope

    @property
    def expires_in(self) -> int:
        return self._token.expires_in

    @property
    def expires_at(self) -> int:
        return self._token.expires_at

    @property
    def refresh_token(self):
        return self._token.refresh_token

    def is_expiring(self) -> bool:
        return self._token.is_expiring()


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


def prompt_for_user_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope=None
) -> RefreshingToken:
    """
    Open a web browser for manual authentication.

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
        automatically refreshing access token
    """
    cred = Credentials(client_id, client_secret, redirect_uri)
    url = cred.user_authorisation_url(scope)

    print('Opening browser for Spotify login...')
    webbrowser.open(url)
    redirected = input('Please paste redirect URL: ').strip()
    code = parse_code_from_url(redirected)
    token = cred.request_user_token(code, scope)
    return RefreshingToken(token, cred)


def token_from_refresh_token(
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
        automatically refreshing access token
    """
    cred = Credentials(client_id, client_secret, redirect_uri)
    token = cred.request_refreshed_token(refresh_token)
    return RefreshingToken(token, cred)
