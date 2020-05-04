from asyncio import run
from unittest import TestCase
from unittest.mock import MagicMock, patch

from tekore import HTTPError, AccessToken, Token, Credentials, Scope
from tests._cred import TestCaseWithEnvironment


class TestAccessToken(TestCase):
    def test_access_token_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AccessToken()

    def test_str_of_access_token_is_value_of_property(self):
        class T(AccessToken):
            @property
            def access_token(self):
                return 'token'

        t = T()
        self.assertEqual(t.access_token, str(t))


def make_token_dict():
    return {
        'access_token': 'accesstoken',
        'expires_in': 3600,
        'token_type': 'tokentype',
        'scope': 'space separated list',
        'refresh_token': 'refreshtoken'
    }


module = 'tekore._auth.expiring'


class TestToken(TestCase):
    def test_access_token_returned(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.access_token, 'accesstoken')

    def test_expires_in_set_time(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.expires_in, 3600)

    def test_expires_in_is_refreshed(self):
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.expires_in, 3599)

    def test_old_token_is_expiring(self):
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch(module + '.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.is_expiring, True)

    def test_token_type(self):
        d = make_token_dict()
        t = Token(d)
        self.assertEqual(t.token_type, d['token_type'])

    def test_scope(self):
        d = make_token_dict()
        t = Token(d)
        self.assertEqual(t.scope, d['scope'])


def mock_response(code: int = 200, content: dict = None) -> MagicMock:
    response = MagicMock()
    response.status_code = code
    response.json = MagicMock(return_value=content or make_token_dict())
    return response


class TestCredentialsOnline(TestCaseWithEnvironment):
    def test_request_client_token(self):
        c = Credentials(self.client_id, self.client_secret)
        c.request_client_token()

    def test_async_request_client_token(self):
        c = Credentials(self.client_id, self.client_secret, asynchronous=True)
        run(c.request_client_token())

    def test_refresh_user_token(self):
        c = Credentials(self.client_id, self.client_secret)
        c.refresh_user_token(self.user_refresh)

    def test_async_refresh_user_token(self):
        c = Credentials(self.client_id, self.client_secret, asynchronous=True)
        run(c.refresh_user_token(self.user_refresh))

    def test_bad_arguments_raises_error(self):
        c = Credentials('id', 'secret')

        with self.assertRaises(HTTPError):
            c.request_client_token()


class TestCredentialsOffline(TestCase):
    def test_credentials_initialisation(self):
        Credentials(client_id='id', client_secret='secret', redirect_uri='uri')

    def test_credentials_init_redirect_uri_optional(self):
        Credentials('id', 'secret')

    def test_server_error_raises_http_error(self):
        c = Credentials('id', 'secret')

        send = MagicMock(return_value=mock_response(500))
        with patch(module + '.Credentials._send', send):
            with self.assertRaises(HTTPError):
                c.request_client_token()

    def test_user_authorisation_url(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url('scope', 'state', True)
        self.assertIn('scope=scope', url)
        self.assertIn('state=state', url)
        self.assertIn('show_dialog=true', url)

    def test_user_authorisation_url_accepts_scope_list(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url(['scope'], 'state', True)
        self.assertIn('scope=scope', url)
        self.assertIn('state=state', url)
        self.assertIn('show_dialog=true', url)

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
            self.assertEqual(refreshed.refresh_token, 'refresh')

    def test_refresh_user_token_refresh_replaced_if_returned(self):
        c = Credentials('id', 'secret', 'uri')
        token = make_token_dict()
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(module + '.Credentials._send', send):
            refreshed = c.refresh_user_token('refresh')
            self.assertEqual(refreshed.refresh_token, token['refresh_token'])

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
