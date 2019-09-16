"""
Utility module for your convenience <3

These functions and classes are meant for local use.
For larger-scale use define your own types and routines,
perhaps based on the ones found in this module.
Particularly ``prompt_for_user_token`` cannot be used if the application
runs on a web server, as it needs to open up a browser.
"""

import os
import webbrowser

from urllib.parse import urlparse, parse_qs
from spotipy.auth import Token, Credentials
from spotipy.scope import Scope


class RefreshingToken:
    """
    Automatically refreshing access token.

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
            self._token = self.credentials.refresh_token(self._token)

        return self._token.access_token

    @property
    def token_type(self):
        return self._token.token_type

    @property
    def scope(self):
        return self._token.scope

    @property
    def expires_in(self):
        return self._token.expires_in

    @property
    def expires_at(self):
        return self._token.expires_at

    @property
    def refresh_token(self):
        return self._token.refresh_token

    def is_expiring(self) -> bool:
        return self._token.is_expiring()


def read_environment(
        client_id_var: str = 'SPOTIPY_CLIENT_ID',
        client_secret_var: str = 'SPOTIPY_CLIENT_SECRET',
        redirect_uri_var: str = 'SPOTIPY_REDIRECT_URI'
) -> (str, str, str):
    """
    Read environment variables for application configuration.

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
    client_id = os.getenv(client_id_var, None)
    client_secret = os.getenv(client_secret_var, None)
    redirect_uri = os.getenv(redirect_uri_var, None)
    return client_id, client_secret, redirect_uri


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
        scope: Scope = None
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
        access rights
    """
    cred = Credentials(client_id, client_secret, redirect_uri)
    url = cred.authorisation_url(scope)

    print('Opening browser for Spotify login...')
    webbrowser.open(url)
    redirected = input('Please paste redirect URL: ').strip()
    code = parse_code_from_url(redirected)
    token = cred.request_access_token(code, scope)
    return RefreshingToken(token, cred)
