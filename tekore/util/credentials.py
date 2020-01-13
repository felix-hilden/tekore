"""
Credentials provides functions for easily retrieving access tokens.

.. code:: python

    from tekore import util

    conf = util.config_from_environment()

    # Request tokens
    app_token = util.request_client_token(*conf[:2])
    user_token = util.prompt_for_user_token(*conf)

    # Reload user token
    user_token = util.refresh_user_token(*conf[:2], refresh_token)
"""

import webbrowser

from urllib.parse import urlparse, parse_qs
from tekore.auth.refreshing import RefreshingToken, RefreshingCredentials


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
    Prompt for manual authentication.

    Open a web browser for the user to log in with Spotify.
    Prompt to paste the URL after logging in to parse the `code` URL parameter.

    Parameters
    ----------
    client_id
        client ID
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
    url = cred.user_authorisation_url(scope, show_dialog=True)

    print('Opening browser for Spotify login...')
    webbrowser.open(url)
    redirected = input('Please paste redirect URL: ').strip()
    code = parse_code_from_url(redirected)
    return cred.request_user_token(code)


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
