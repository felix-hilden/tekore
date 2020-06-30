import time

from abc import ABC, abstractmethod
from base64 import b64encode as _b64encode
from typing import Union

from urllib.parse import urlencode

from .scope import Scope
from .._error import get_error
from .._sender import Sender, Client, send_and_process, Request, Response

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


def b64encode(msg: str) -> str:
    """Encode a unicode string in base-64."""
    return _b64encode(msg.encode()).decode()


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

    def __str__(self):
        """Bearer token value."""
        return self.access_token


class Token(AccessToken):
    """
    Expiring access token.

    Represents both client and user tokens.
    The refresh token of a client token is ``None``.
    """

    def __init__(self, token_info: dict):
        self._access_token = token_info['access_token']
        self._token_type = token_info['token_type']

        self._scope = Scope(*token_info['scope'].split(' '))
        if str(self._scope) == '':
            self._scope = Scope()

        self._refresh_token = token_info.get('refresh_token', None)
        self._expires_at = int(time.time()) + token_info['expires_in']

    def __repr__(self):
        options = [
            f'access_token={self.access_token!r}',
            f'refresh_token={self.refresh_token!r}',
            f'expires_at={self.expires_at!r}',
            f'scope={self.scope!r}',
        ]
        return type(self).__name__ + '(' + ', '.join(options) + ')'

    @property
    def access_token(self) -> str:
        """Bearer token value."""
        return self._access_token

    @property
    def refresh_token(self) -> Union[str, None]:
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
        return self.expires_in < 60


def handle_errors(request: Request, response: Response) -> None:
    """Examine response and raise errors accordingly."""
    if response.status_code < 400:
        return

    if response.status_code < 500:
        error_str = f"{response.status_code} {response.content['error']}"
        description = response.content.get('error_description', None)
        if description is not None:
            error_str += ': ' + description
    else:
        error_str = 'Unexpected error!'

    error_cls = get_error(response.status_code)
    raise error_cls(error_str, request=request, response=response)


def parse_token(request: Request, response: Response) -> Token:
    """Parse token object from response."""
    handle_errors(request, response)
    return Token(response.content)


def parse_refreshed_token(
    request: Request, response: Response, refresh_token: str
) -> Token:
    """Replace new refresh token with old value if empty."""
    refreshed = parse_token(request, response)

    if refreshed.refresh_token is None:
        refreshed._refresh_token = refresh_token

    return refreshed


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

    def __repr__(self):
        options = [
            f'client_id={self.client_id!r}',
            f'client_secret={self.client_secret!r}',
            f'redirect_uri={self.redirect_uri!r}',
            f'sender={self.sender!r}',
        ]
        return type(self).__name__ + '(' + ', '.join(options) + ')'

    @property
    def _auth(self) -> str:
        return b64encode(self.client_id + ':' + self.client_secret)

    def _token_request(self, payload: dict):
        headers = {'Authorization': f'Basic {self._auth}'}
        return Request('POST', OAUTH_TOKEN_URL, data=payload, headers=headers)

    @send_and_process(parse_token)
    def request_client_token(self) -> Token:
        """
        Request a client token.

        Returns
        -------
        Token
            client access token
        """
        payload = {'grant_type': 'client_credentials'}
        return self._token_request(payload), ()

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
        payload = {
            'show_dialog': str(show_dialog).lower(),
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri
        }
        if isinstance(scope, list):
            scope = Scope(*scope)
        if scope is not None:
            payload['scope'] = str(scope)
        if state is not None:
            payload['state'] = state

        return OAUTH_AUTHORIZE_URL + '?' + urlencode(payload)

    @send_and_process(parse_token)
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
        return self._token_request(payload), ()

    @send_and_process(parse_refreshed_token)
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
        return self._token_request(payload), (refresh_token,)

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
