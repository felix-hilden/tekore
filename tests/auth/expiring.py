import pytest

from unittest import TestCase
from unittest.mock import MagicMock, patch

from tekore import HTTPError, AccessToken, Token, Credentials, Scope


class TestAccessToken:
    def test_access_token_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            AccessToken()

    def test_str_of_access_token_is_value_of_property(self):
        class T(AccessToken):
            @property
            def access_token(self):
                return 'token'

        t = T()
        assert t.access_token == str(t)


def make_token_dict():
    return {
        'access_token': 'accesstoken',
        'expires_in': 3600,
        'token_type': 'tokentype',
        'scope': 'space separated list',
        'refresh_token': 'refreshtoken'
    }


module = 'tekore._auth.expiring'


class TestToken:
    def test_access_token_returned(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            assert token.access_token == 'accesstoken'

    def test_expires_in_set_time(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            assert token.expires_in == 3600

    def test_expires_in_is_refreshed(self):
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            assert token.expires_in == 3599

    def test_old_token_is_expiring(self):
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            assert token.is_expiring is True

    def test_token_type(self):
        d = make_token_dict()
        t = Token(d)
        assert t.token_type == d['token_type']

    def test_scope_parsed(self):
        d = make_token_dict()
        scope = 'a b c'
        d['scope'] = scope
        t = Token(d)

        assert isinstance(t.scope, Scope)
        assert str(t.scope) == scope

    def test_no_scope_is_empty(self):
        d = make_token_dict()
        scope = ''
        d['scope'] = scope
        t = Token(d)

        assert len(t.scope) == 0


def mock_response(code: int = 200, content: dict = None) -> MagicMock:
    response = MagicMock()
    response.status_code = code
    response.json = MagicMock(return_value=content or make_token_dict())
    return response


class TestCredentialsOnline:
    def test_request_client_token(self, app_env):
        c = Credentials(app_env[0], app_env[1])
        token = c.request_client_token()
        assert token.refresh_token is None

    @pytest.mark.asyncio
    async def test_async_request_client_token(self, app_env):
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.request_client_token()
        assert token.refresh_token is None

    def test_refresh_user_token(self, app_env, user_refresh):
        c = Credentials(app_env[0], app_env[1])
        token = c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None

    @pytest.mark.asyncio
    async def test_async_refresh_user_token(self, app_env, user_refresh):
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None

    def test_bad_arguments_raises_error(self):
        c = Credentials('id', 'secret')

        with pytest.raises(HTTPError):
            c.request_client_token()


class TestCredentialsOffline:
    def test_credentials_initialisation(self):
        Credentials(client_id='id', client_secret='secret', redirect_uri='uri')

    def test_credentials_init_redirect_uri_optional(self):
        Credentials('id', 'secret')

    def test_server_error_raises_http_error(self):
        c = Credentials('id', 'secret')

        send = MagicMock(return_value=mock_response(500))
        with patch(module + '.Credentials._send', send):
            with pytest.raises(HTTPError):
                c.request_client_token()

    def test_user_authorisation_url(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url('scope', 'state', True)
        assert 'scope=scope' in url
        assert 'state=state' in url
        assert 'show_dialog=true' in url

    def test_user_authorisation_url_accepts_scope_list(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url(['a', 'b'], 'state', True)
        assert 'scope=a+b' in url

    def test_request_user_token(self):
        c = Credentials('id', 'secret', 'uri')
        send = MagicMock(return_value=mock_response())
        with patch(module + '.Credentials._send', send):
            c.request_user_token('code')
            send.assert_called_once()

    def test_refresh_user_token_uses_old_refresh_if_not_returned(self):
        c = Credentials('id', 'secret', 'uri')
        token = make_token_dict()
        token['refresh_token'] = None
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(module + '.Credentials._send', send):
            refreshed = c.refresh_user_token('refresh')
            assert refreshed.refresh_token == 'refresh'

    def test_refresh_user_token_refresh_replaced_if_returned(self):
        c = Credentials('id', 'secret', 'uri')
        token = make_token_dict()
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(module + '.Credentials._send', send):
            refreshed = c.refresh_user_token('refresh')
            assert refreshed.refresh_token == token['refresh_token']

    def test_refresh_none_refresh_interpreted_as_client_token(self):
        c = Credentials('id', 'secret', 'uri')
        token = MagicMock()
        token.refresh_token = None

        mock = MagicMock()
        with patch(module + '.Credentials.request_client_token', mock):
            c.refresh(token)
            mock.assert_called_once()

    def test_refresh_valid_refresh_interpreted_as_user_token(self):
        c = Credentials('id', 'secret', 'uri')
        token = MagicMock()
        token.refresh_token = 'refresh'

        mock = MagicMock()
        with patch(module + '.Credentials.refresh_user_token', mock):
            c.refresh(token)
            mock.assert_called_once()
