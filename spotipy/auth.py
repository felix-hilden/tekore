"""
OAuth2 authentication for client credentials and authorisation code.
"""

import time
import requests

from abc import ABC, abstractmethod
from base64 import b64encode as _b64encode
from urllib.parse import urlencode

from spotipy.scope import Scope

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


class OAuthError(requests.HTTPError):
    pass


def b64encode(msg: str) -> str:
    """
    Base 64 encoding for Unicode strings.
    """
    return _b64encode(msg.encode()).decode()


class AccessToken(ABC):
    """
    Token object.

    Has an 'access_token' property, which is also
    the string representation of the instance.
    """
    @property
    @abstractmethod
    def access_token(self) -> str:
        pass

    def __str__(self):
        return self.access_token


class Token(AccessToken):
    """
    Spotify OAuth access token.
    """
    def __init__(self, token_info: dict):
        self._access_token = token_info['access_token']
        self._expires_in = token_info['expires_in']
        self.token_type = token_info['token_type']
        self.scope = token_info['scope']

        self.refresh_token = token_info.get('refresh_token', None)
        self.expires_at = int(time.time()) + token_info['expires_in']

    @property
    def access_token(self) -> str:
        """
        Bearer token value.
        """
        return self._access_token

    @property
    def expires_in(self) -> int:
        """
        Seconds until token expiration.
        """
        return self.expires_at - int(time.time())

    def is_expiring(self) -> bool:
        """
        Determine whether token is about to expire.
        """
        return self.expires_in < 60


class Credentials:
    """
    Client for retrieving access tokens.

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
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def request_client_credentials(self) -> Token:
        """
        Request for access token using application credentials.

        Returns
        -------
        Token
            application access token
        """
        payload = {'grant_type': 'client_credentials'}
        return self._post_token_request(payload)

    def authorisation_url(self, scope: Scope = None, state: str = None) -> str:
        """
        Construct an authorisation URL for Spotify login.

        Parameters
        ----------
        scope
            access rights
        state
            additional state

        Returns
        -------
        str
            URL for Spotify login
        """
        payload = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri
        }

        if scope is not None:
            payload['scope'] = str(scope)
        if state is not None:
            payload['state'] = state

        return OAUTH_AUTHORIZE_URL + '?' + urlencode(payload)

    def _post_token_request(self, payload: dict) -> Token:
        auth_header = b64encode(self.client_id + ':' + self.client_secret)
        headers = {'Authorization': f'Basic {auth_header}'}
        response = requests.post(
            OAUTH_TOKEN_URL, data=payload, headers=headers
        )

        if response.status_code != 200:
            raise OAuthError(
                f'Access token request failed: '
                f'{response.status_code}, {response.reason}'
            )

        return Token(response.json())

    def request_access_token(
            self,
            code: str,
            scope: Scope = None,
            state: str = None
    ) -> Token:
        """
        Request for access token using a code
        provided by a request from the Spotify server.

        Parameters
        ----------
        code
            code from request parameters
        scope
            access rights
        state
            additional state

        Returns
        -------
        Token
            user access token
        """
        payload = {
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        if scope is not None:
            payload['scope'] = str(scope)
        if state is not None:
            payload['state'] = state

        return self._post_token_request(payload)

    def refresh_token(self, token: Token) -> Token:
        """
        Request a refreshed access token.

        Parameters
        ----------
        token
            token to be refreshed

        Returns
        -------
        Token
            refreshed access token
        """
        payload = {
            'refresh_token': token.refresh_token,
            'grant_type': 'refresh_token'
        }

        refreshed = self._post_token_request(payload)

        if refreshed.refresh_token is None:
            refreshed.refresh_token = token.refresh_token

        return refreshed
