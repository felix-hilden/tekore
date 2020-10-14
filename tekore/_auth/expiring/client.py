from base64 import b64encode as _b64encode
from typing import Tuple
from hashlib import sha256
from secrets import token_urlsafe

from urllib.parse import urlencode

from .decor import parse_token, parse_refreshed_token
from .token import Token
from ..scope import Scope
from ..._sender import Sender, Client, send_and_process, Request

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


def b64encode(msg: str) -> str:
    """Encode a unicode string in base-64."""
    return _b64encode(msg.encode()).decode()


def b64urlencode(msg: bytes) -> str:
    """Encode bytes in url-safe base-64 alphabet."""
    encoded = _b64encode(msg).decode()
    stripped = encoded.split("=")[0]
    return stripped.replace("+", "-").replace("/", "_")


class Credentials(Client):
    """
    Client for retrieving access tokens.

    Parameters
    ----------
    client_id
        client id
    client_secret
        client secret, not required for PKCE user authorisation
    redirect_uri
        whitelisted redirect URI, required for user authorisation
    sender
        request sender
    asynchronous
        synchronicity requirement
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str = None,
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

    def _token_request(self, payload: dict, auth: bool) -> Request:
        if auth:
            if self.client_secret is None:
                raise ValueError(
                    f'A client secret is required! Got `{self.client_secret}`.'
                )
            token = b64encode(self.client_id + ':' + self.client_secret)
            headers = {'Authorization': f'Basic {token}'}
        else:
            headers = None

        return Request('POST', OAUTH_TOKEN_URL, data=payload, headers=headers)

    @send_and_process(parse_token(uses_pkce=False))
    def request_client_token(self) -> Token:
        """
        Request a client token.

        Returns
        -------
        Token
            client access token
        """
        payload = {'grant_type': 'client_credentials'}
        return self._token_request(payload, auth=True), ()

    def _user_auth_payload(self, scope, state):
        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
        }
        if isinstance(scope, list):
            scope = Scope(*scope)
        if scope is not None:
            payload['scope'] = str(scope)
        if state is not None:
            payload['state'] = state
        return payload

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
        payload = self._user_auth_payload(scope, state)
        payload['show_dialog'] = str(show_dialog).lower()
        return OAUTH_AUTHORIZE_URL + '?' + urlencode(payload)

    @send_and_process(parse_token(uses_pkce=False))
    def request_user_token(self, code: str) -> Token:
        """
        Request a new user token.

        Step 2/2 in authorisation code flow.
        Code is provided as a URL parameter in the redirect URI
        after login in step 1: :meth:`user_authorisation_url`.

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
        return self._token_request(payload, auth=True), ()

    @send_and_process(parse_refreshed_token(uses_pkce=False))
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
        return self._token_request(payload, auth=True), (refresh_token,)

    def pkce_user_authorisation(
        self,
        scope=None,
        state: str = None,
        verifier_bytes: int = 32,
    ) -> Tuple[str, str]:
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
        Tuple[str, str]
            authorisation URL and PKCE code verifier
        """
        assert 32 <= verifier_bytes <= 96, 'Invalid number of verifier bytes!'
        verifier = token_urlsafe(verifier_bytes)

        sha = sha256(verifier.encode())
        challenge = b64urlencode(sha.digest())

        payload = self._user_auth_payload(scope, state)
        payload['code_challenge'] = challenge
        payload['code_challenge_method'] = 'S256'

        auth_url = OAUTH_AUTHORIZE_URL + '?' + urlencode(payload)
        return auth_url, verifier

    @send_and_process(parse_token(uses_pkce=True))
    def request_pkce_token(self, code: str, verifier: str) -> Token:
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
        Token
            user access token
        """
        payload = {
            'client_id': self.client_id,
            'code': code,
            'code_verifier': verifier,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        }
        return self._token_request(payload, auth=False), ()

    @send_and_process(parse_refreshed_token(uses_pkce=True))
    def refresh_pkce_token(self, refresh_token: str) -> Token:
        """
        Request a refreshed PKCE user token.

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
            'client_id': self.client_id,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return self._token_request(payload, auth=False), (refresh_token,)

    def refresh(self, token: Token) -> Token:
        """
        Refresh an access token.

        Both client and user tokens are accepted and refreshed.
        The correct refreshing method is applied regardless if PKCE was used or not.
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
        elif token.uses_pkce:
            return self.refresh_pkce_token(token.refresh_token)
        else:
            return self.refresh_user_token(token.refresh_token)
