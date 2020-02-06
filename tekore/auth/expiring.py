import time

from abc import ABC, abstractmethod
from base64 import b64encode as _b64encode
from typing import Callable
from functools import wraps

from requests import HTTPError, Request, Response
from urllib.parse import urlencode

from tekore.sender import Sender, Client

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


class OAuthError(HTTPError):
    pass


def b64encode(msg: str) -> str:
    """
    Base 64 encoding for Unicode strings.
    """
    return _b64encode(msg.encode()).decode()


class AccessToken(ABC):
    """
    Token object.
    """
    @property
    @abstractmethod
    def access_token(self) -> str:
        """
        Bearer token value.

        Used as the string representation of the instance.
        """
        raise NotImplementedError

    def __str__(self):
        return self.access_token


class Token(AccessToken):
    """
    Spotify OAuth access token.

    Represents both client and user tokens.
    The refresh token of a client token is ``None``.
    """
    def __init__(self, token_info: dict):
        self._access_token = token_info['access_token']
        self._token_type = token_info['token_type']
        self._scope = token_info['scope']

        self._refresh_token = token_info.get('refresh_token', None)
        self._expires_at = int(time.time()) + token_info['expires_in']

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def expires_in(self) -> int:
        """
        Seconds until token expiration.
        """
        return self.expires_at - int(time.time())

    @property
    def expires_at(self) -> int:
        return self._expires_at

    @property
    def is_expiring(self) -> bool:
        """
        Determine whether token is about to expire.
        """
        return self.expires_in < 60


def handle_errors(response: Response) -> None:
    if 400 <= response.status_code < 500:
        content = response.json()
        error_str = '{} {}: {}'.format(
            response.status_code,
            content['error'],
            content['error_description']
        )
        raise OAuthError(error_str)
    elif response.status_code >= 500:
        raise HTTPError('Unexpected error!', response=response)


def parse_token(response):
    handle_errors(response)
    content = response.json()
    return Token(content)


def send_and_process_token(
        function: Callable[..., Request]
) -> Callable[..., Token]:
    async def async_send(self, request: Request):
        response = await self._send(request)
        return parse_token(response)

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        request = function(self, *args, **kwargs)

        if self.is_async:
            return async_send(self, request)

        response = self._send(request)
        return parse_token(response)
    return wrapper


def parse_refreshed_token(response, refresh_token: str) -> Token:
    refreshed = parse_token(response)

    if refreshed.refresh_token is None:
        refreshed._refresh_token = refresh_token

    return refreshed


def send_and_process_refreshed_token(
        function: Callable[..., Request]
) -> Callable[..., Token]:
    async def async_send(self, request: Request, refresh_token: str):
        response = await self._send(request)
        return parse_refreshed_token(response, refresh_token)

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        request, refresh_token = function(self, *args, **kwargs)

        if self.is_async:
            return async_send(self, request, refresh_token)

        response = self._send(request)
        return parse_refreshed_token(response, refresh_token)
    return wrapper


class Credentials(Client):
    """
    Client for retrieving access tokens.

    Specifying a ``redirect_uri`` is required only when authorising users.

    Parameters
    ----------
    client_id
        client id
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    sender
        request sender
    asynchronous
        synchronicity requirement
    """
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str = None,
            sender: Sender = None,
            asynchronous: bool = None,
    ):
        super().__init__(sender, asynchronous)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @property
    def _auth(self) -> str:
        return b64encode(self.client_id + ':' + self.client_secret)

    def _request_token(self, payload: dict):
        headers = {'Authorization': f'Basic {self._auth}'}
        return Request('POST', OAUTH_TOKEN_URL, data=payload, headers=headers)

    @send_and_process_token
    def request_client_token(self) -> Token:
        """
        Request a client token.

        Returns
        -------
        Token
            client access token
        """
        payload = {'grant_type': 'client_credentials'}
        return self._request_token(payload)

    def user_authorisation_url(
            self,
            scope=None,
            state: str = None,
            show_dialog: bool = False
    ) -> str:
        """
        Construct an authorisation URL.

        Step 1/2 in authorisation code flow.
        User should be redirected to the resulting URL for authorisation.

        Parameters
        ----------
        scope
            access rights as a space-separated list
        state
            additional state
        show_dialog
            force login dialog even if previously authorised

        Returns
        -------
        str
            login URL
        """
        payload = {
            'show_dialog': str(show_dialog).lower(),
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri
        }

        if scope is not None:
            payload['scope'] = str(scope)
        if state is not None:
            payload['state'] = state

        return OAUTH_AUTHORIZE_URL + '?' + urlencode(payload)

    @send_and_process_token
    def request_user_token(self, code: str) -> Token:
        """
        Request a new user token.

        Step 2/2 in authorisation code flow.
        Code is provided as a URL parameter in the redirect URI
        after login in step 1.

        Parameters
        ----------
        code
            code from redirect parameters

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
        return self._request_token(payload)

    @send_and_process_refreshed_token
    def refresh_user_token(self, refresh_token: str) -> Token:
        """
        Request a refreshed user token.

        Parameters
        ----------
        refresh_token
            refresh token

        Returns
        -------
        Token
            refreshed user access token
        """
        payload = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        return self._request_token(payload), refresh_token

    def refresh(self, token: Token) -> Token:
        """
        Refresh an access token.

        Both client and user tokens are accepted and refreshed.
        For client tokens, a new token is returned.
        For user tokens, a refreshed token is returned.

        Parameters
        ----------
        token
            token to be refreshed

        Returns
        -------
        Token
            refreshed access token
        """
        if token.refresh_token is None:
            return self.request_client_token()
        else:
            return self.refresh_user_token(token.refresh_token)
