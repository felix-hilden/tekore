import pytest

from unittest.mock import MagicMock, patch
from tekore import HTTPError, AccessToken, Token, Credentials, Scope, Response


class TestAccessToken:
    def test_access_token_cannot_be_instantiated(self):
        """
        Test if the access_cannot.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(TypeError):
            AccessToken()

    def test_str_of_access_token_is_value_of_property(self):
        """
        Returns a string of access token access token.

        Args:
            self: (todo): write your description
        """
        class T(AccessToken):
            @property
            def access_token(self):
                """
                Returns an access token.

                Args:
                    self: (todo): write your description
                """
                return 'token'

        t = T()
        assert t.access_token == str(t)


def token_dict():
    """
    Returns a dictionary to a dictionary.

    Args:
    """
    return {
        'access_token': 'accesstoken',
        'expires_in': 3600,
        'token_type': 'tokentype',
        'scope': 'space separated list',
        'refresh_token': 'refreshtoken'
    }


def make_token(attrs: dict = None, uses_pkce: bool = False):
    """
    Create a token from a dictionary.

    Args:
        attrs: (dict): write your description
        uses_pkce: (bool): write your description
    """
    a = token_dict()
    a.update(attrs or {})
    return Token(a, uses_pkce)


time_module = 'tekore._auth.expiring.token.time'


class TestToken:
    def test_repr(self):
        """
        R

        Args:
            self: (todo): write your description
        """
        t = make_token()
        assert repr(t).startswith('Token(')

    def test_access_token_returned(self):
        """
        Returns the access token.

        Args:
            self: (todo): write your description
        """
        time = MagicMock()
        time.time.return_value = 0

        with patch(time_module, time):
            token = make_token()
            assert token.access_token == 'accesstoken'

    def test_expires_in_set_time(self):
        """
        Test if the set time of the test.

        Args:
            self: (todo): write your description
        """
        time = MagicMock()
        time.time.return_value = 0

        with patch(time_module, time):
            token = make_token()
            assert token.expires_in == 3600

    def test_expires_in_is_refreshed(self):
        """
        Checks if the token is in the token.

        Args:
            self: (todo): write your description
        """
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch(time_module, time):
            token = make_token()
            assert token.expires_in == 3599

    def test_old_token_is_expiring(self):
        """
        Check if the token is locked.

        Args:
            self: (todo): write your description
        """
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch(time_module, time):
            token = make_token()
            assert token.is_expiring is True

    def test_token_type(self):
        """
        Set the token_type of a token.

        Args:
            self: (todo): write your description
        """
        t = make_token()
        assert isinstance(t.token_type, str)

    def test_scope_parsed(self):
        """
        Test if the current scope is valid.

        Args:
            self: (todo): write your description
        """
        t = make_token()
        assert isinstance(t.scope, Scope)

    def test_no_scope_is_empty(self):
        """
        Returns true if the scope is not empty.

        Args:
            self: (todo): write your description
        """
        t = make_token({'scope': ''})
        assert len(t.scope) == 0


def mock_response(code: int = 200, content: dict = None) -> MagicMock:
    """
    Makes a response. response.

    Args:
        code: (str): write your description
        content: (str): write your description
    """
    return Response('https://url.com', {}, code, content or token_dict())


class TestCredentialsOnline:
    def test_request_client_token(self, app_env):
        """
        Test if a request.

        Args:
            self: (todo): write your description
            app_env: (todo): write your description
        """
        c = Credentials(app_env[0], app_env[1])
        token = c.request_client_token()
        assert token.refresh_token is None

    @pytest.mark.asyncio
    async def test_async_request_client_token(self, app_env):
          """
          Requests session token.

          Args:
              self: (todo): write your description
              app_env: (todo): write your description
          """
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.request_client_token()
        assert token.refresh_token is None
        await c.close()

    def test_refresh_user_token(self, app_env, user_refresh):
        """
        Refresh the access token.

        Args:
            self: (todo): write your description
            app_env: (todo): write your description
            user_refresh: (bool): write your description
        """
        c = Credentials(app_env[0], app_env[1])
        token = c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None

    @pytest.mark.asyncio
    async def test_async_refresh_user_token(self, app_env, user_refresh):
          """
          Refresh the user token.

          Args:
              self: (todo): write your description
              app_env: (todo): write your description
              user_refresh: (todo): write your description
          """
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None
        await c.close()

    def test_bad_arguments_raises_error(self):
        """
        Test if an error is enabled.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')

        with pytest.raises(HTTPError):
            c.request_client_token()


cred_module = 'tekore._auth.expiring.Credentials'


class TestCredentialsOffline:
    def test_repr(self):
        """
        Test the current credentials.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        assert repr(c).startswith('Credentials(')

    def test_credentials_initialisation(self):
        """
        Initialize the credentials credentials.

        Args:
            self: (todo): write your description
        """
        Credentials(client_id='id', client_secret='secret', redirect_uri='uri')

    def test_credentials_only_client_id_mandatory(self):
        """
        Test if the client credentials are enabled.

        Args:
            self: (todo): write your description
        """
        Credentials('id')

    def test_basic_token_with_no_secret_raises(self):
        """
        Test if a request token is valid.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id')
        with pytest.raises(ValueError):
            c.request_client_token()

    def test_server_error_raises_http_error(self):
        """
        Gets an oauth token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        response = mock_response(500, {})
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()

    def test_client_error_with_description(self):
        """
        Gets an oauth client token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        error = {'error': 'Bad thing', 'error_description': 'because reasons'}
        response = mock_response(400, error)
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()

    def test_client_error_without_description(self):
        """
        Gets a client description of the oauth client.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        error = {'error': 'Bad thing'}
        response = mock_response(400, error)
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()

    def test_user_authorisation_url(self):
        """
        Gets the user s3 url to.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', redirect_uri='uri')
        url = c.user_authorisation_url('scope', 'state')
        assert 'scope=scope' in url
        assert 'state=state' in url

    def test_user_authorisation_accepts_scope_list(self):
        """
        Gets the list of the authenticated user user access token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', redirect_uri='uri')
        url = c.user_authorisation_url(['a', 'b'], 'state')
        assert 'scope=a+b' in url

    def test_request_user_token(self):
        """
        Request the token for the user authentication.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret', 'uri')
        send = MagicMock(return_value=mock_response())
        with patch(cred_module + '.send', send):
            c.request_user_token('code')
            send.assert_called_once()

    def test_refresh_user_token_uses_old_refresh_if_not_returned(self):
        """
        Refresh the refresh token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        token = token_dict()
        token['refresh_token'] = None
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(cred_module + '.send', send):
            refreshed = c.refresh_user_token('refresh')
            assert refreshed.refresh_token == 'refresh'

    def test_refresh_user_token_refresh_replaced_if_returned(self):
        """
        Refresh a refresh token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        token = token_dict()
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(cred_module + '.send', send):
            refreshed = c.refresh_user_token('refresh')
            assert refreshed.refresh_token == token['refresh_token']

    def test_pkce_user_authorisation(self):
        """
        Handle the user credentials that the admin.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', redirect_uri='redirect')
        c.pkce_user_authorisation('scope', 'state')

    def test_request_pkce_token(self):
        """
        Returns a request token for a request.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id')
        c.send = MagicMock(return_value=mock_response())
        token = c.request_pkce_token('scope', 'verifier')
        assert token.uses_pkce

    def test_refresh_pkce_token(self):
        """
        Returns a refresh token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id')
        c.send = MagicMock(return_value=mock_response())
        token = c.refresh_pkce_token('refresh')
        assert token.uses_pkce

    def test_auto_refresh_client_token(self):
        """
        Test if a refresh token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        token = make_token({'refresh_token': None})
        c.request_client_token = MagicMock(return_value=token)
        c.refresh(token)
        c.request_client_token.assert_called_once()

    def test_auto_refresh_user_token(self):
        """
        Test if the access token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id', 'secret')
        token = make_token(uses_pkce=False)
        c.refresh_user_token = MagicMock(return_value=token)
        c.refresh(token)
        c.refresh_user_token.assert_called_once()

    def test_auto_refresh_pkce_token(self):
        """
        Refresh refresh token.

        Args:
            self: (todo): write your description
        """
        c = Credentials('id')
        token = make_token(uses_pkce=True)
        c.refresh_pkce_token = MagicMock(return_value=token)
        c.refresh(token)
        c.refresh_pkce_token.assert_called_once()
