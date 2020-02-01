from tekore.auth.expiring import AccessToken, Token, Credentials
from tekore.sender import SyncSender


class RefreshingToken(AccessToken):
    """
    Automatically refreshing access token.

    Returned from utility functions and :class:`RefreshingCredentials`.
    It shouldn't have to be instantiated outside of the functions,
    unless you are sure that you want to.

    Uses an instance of
    :class:`Credentials <tekore.auth.expiring.Credentials>`
    to automatically request a new access token
    when the old one is about to expire.
    This occurs when the `access_token` property is read.

    Both :attr:`expires_in` and :attr:`expires_at` are always ``None``,
    and :attr:`is_expiring` is always ``False``.

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
        if self._token.is_expiring:
            self._token = self._credentials.refresh(self._token)

        return self._token.access_token

    @property
    def refresh_token(self) -> str:
        return self._token.refresh_token

    @property
    def token_type(self) -> str:
        return self._token.token_type

    @property
    def scope(self) -> str:
        return self._token.scope

    @property
    def expires_in(self) -> None:
        return None

    @property
    def expires_at(self) -> None:
        return None

    @property
    def is_expiring(self) -> bool:
        return False


class RefreshingCredentials:
    """
    Synchronous client for retrieving automatically refreshing access tokens.

    Delegates to an underlying
    :class:`Credentials <tekore.auth.expiring.Credentials>`
    manager and parses tokens it returns into :class:`RefreshingToken`.

    Parameters
    ----------
    client_id
        client id
    client_secret
        client secret
    redirect_uri
        whitelisted redirect URI
    sender
        synchronous request sender
    """
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str = None,
            sender: SyncSender = None
    ):
        self._client = Credentials(
            client_id,
            client_secret,
            redirect_uri,
            sender,
            asynchronous=False
        )

    def request_client_token(self) -> RefreshingToken:
        """
        Request a refreshing client token.

        Returns
        -------
        RefreshingToken
            automatically refreshing client token
        """
        token = self._client.request_client_token()
        return RefreshingToken(token, self._client)

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
        return self._client.user_authorisation_url(scope, state, show_dialog)

    def request_user_token(self, code: str) -> RefreshingToken:
        """
        Request a new refreshing user token.

        Step 2/2 in authorisation code flow.
        Code is provided as a URL parameter in the redirect URI
        after login in step 1.

        Parameters
        ----------
        code
            code from redirect parameters

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self._client.request_user_token(code)
        return RefreshingToken(token, self._client)

    def refresh_user_token(self, refresh_token: str) -> RefreshingToken:
        """
        Request an automatically refreshing user token with a refresh token.

        Parameters
        ----------
        refresh_token
            refresh token

        Returns
        -------
        RefreshingToken
            automatically refreshing user token
        """
        token = self._client.refresh_user_token(refresh_token)
        return RefreshingToken(token, self._client)
