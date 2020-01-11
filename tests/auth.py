import unittest
from unittest.mock import MagicMock, patch

from requests import HTTPError
from spotipy.auth.expiring import AccessToken, Token, Credentials, OAuthError
from spotipy.auth.refreshing import RefreshingCredentials, RefreshingToken

from tests.client._cred import TestCaseWithEnvironment, TestCaseWithCredentials


class TestAccessToken(unittest.TestCase):
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


class TestToken(unittest.TestCase):
    def test_access_token_returned(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch('spotipy.auth.expiring.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.access_token, 'accesstoken')

    def test_expires_in_set_time(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch('spotipy.auth.expiring.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.expires_in, 3600)

    def test_expires_in_is_refreshed(self):
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch('spotipy.auth.expiring.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.expires_in, 3599)

    def test_old_token_is_expiring(self):
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch('spotipy.auth.expiring.time', time):
            token = Token(make_token_dict())
            self.assertEqual(token.is_expiring, True)


def mock_response(code: int = 200, content: dict = None) -> MagicMock:
    response = MagicMock()
    response.status_code = code
    response.json = MagicMock(return_value=content or make_token_dict())
    return response


class TestCredentialsOnline(TestCaseWithEnvironment):
    def test_request_client_token(self):
        c = Credentials(self.client_id, self.client_secret)
        c.request_client_token()

    def test_refresh_user_token(self):
        c = Credentials(self.client_id, self.client_secret)
        c.refresh_user_token(self.user_refresh)

    def test_bad_arguments_raises_oauth_error(self):
        c = Credentials('id', 'secret')

        with self.assertRaises(OAuthError):
            c.request_client_token()


class TestCredentialsOffline(unittest.TestCase):
    def test_credentials_initialisation(self):
        Credentials(client_id='id', client_secret='secret', redirect_uri='uri')

    def test_credentials_init_redirect_uri_optional(self):
        Credentials('id', 'secret')

    def test_server_error_raises_http_error(self):
        c = Credentials('id', 'secret')

        send = MagicMock(return_value=mock_response(500))
        with patch('spotipy.auth.Credentials._send', send):
            with self.assertRaises(HTTPError):
                c.request_client_token()

    def test_user_authorisation_url(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url('scope', 'state', True)
        self.assertIn('scope=scope', url)
        self.assertIn('state=state', url)
        self.assertIn('show_dialog=true', url)

    def test_request_user_token(self):
        c = Credentials('id', 'secret', 'uri')
        send = MagicMock(return_value=mock_response())
        with patch('spotipy.auth.Credentials._send', send):
            c.request_user_token('code')
            send.assert_called_once()

    def test_refresh_user_token_uses_old_refresh_if_not_returned(self):
        c = Credentials('id', 'secret', 'uri')
        token = make_token_dict()
        token['refresh_token'] = None
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch('spotipy.auth.Credentials._send', send):
            refreshed = c.refresh_user_token('refresh')
            self.assertEqual(refreshed.refresh_token, 'refresh')

    def test_refresh_user_token_refresh_replaced_if_returned(self):
        c = Credentials('id', 'secret', 'uri')
        token = make_token_dict()
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch('spotipy.auth.Credentials._send', send):
            refreshed = c.refresh_user_token('refresh')
            self.assertEqual(refreshed.refresh_token, token['refresh_token'])

    def test_refresh_none_refresh_interpreted_as_client_token(self):
        c = Credentials('id', 'secret', 'uri')
        token = MagicMock()
        token.refresh_token = None

        mock = MagicMock()
        with patch('spotipy.auth.Credentials.request_client_token', mock):
            c.refresh(token)
            mock.assert_called_once()

    def test_refresh_valid_refresh_interpreted_as_user_token(self):
        c = Credentials('id', 'secret', 'uri')
        token = MagicMock()
        token.refresh_token = 'refresh'

        mock = MagicMock()
        with patch('spotipy.auth.Credentials.refresh_user_token', mock):
            c.refresh(token)
            mock.assert_called_once()


def make_token_obj(value: str, expiring: bool):
    token = MagicMock()
    token.is_expiring = expiring
    token.access_token = value
    return token


class TestRefreshingToken(unittest.TestCase):
    def test_fresh_token_returned(self):
        low_token = make_token_obj('token', False)
        cred = MagicMock()

        auto_token = RefreshingToken(low_token, cred)
        self.assertEqual(auto_token.access_token, 'token')

    def test_expiring_token_refreshed(self):
        expiring = make_token_obj('expiring', True)
        refreshed = make_token_obj('refreshed', False)
        cred = MagicMock()
        cred.refresh.return_value = refreshed

        auto_token = RefreshingToken(expiring, cred)
        self.assertEqual(auto_token.access_token, 'refreshed')

    def test_refreshing_token_has_same_attributes_as_regular(self):
        token_info = MagicMock()
        token = Token(token_info)
        token._expires_at = 3000
        auto_token = RefreshingToken(token, MagicMock())

        token_attributes = [a for a in dir(token) if not a.startswith('_')]
        auto_attributes = [a for a in dir(auto_token) if not a.startswith('_')]

        for attribute in token_attributes:
            with self.subTest(f'Attribute: `{attribute}`'):
                auto_token.__getattribute__(attribute)
                self.assertTrue(attribute in auto_attributes)

    def test_refreshing_token_expiration_attributes(self):
        token_info = MagicMock()
        token = Token(token_info)
        token._expires_at = 0

        auto_token = RefreshingToken(token, MagicMock())
        with self.subTest('is_expiring is False'):
            self.assertFalse(auto_token.is_expiring)
        with self.subTest('expires_in is None'):
            self.assertIsNone(auto_token.expires_in)
        with self.subTest('expires_at is None'):
            self.assertIsNone(auto_token.expires_at)


class TestRefreshingCredentials(TestCaseWithCredentials):
    def _initialise(self):
        return RefreshingCredentials(
            self.client_id,
            self.client_secret,
            self.redirect_uri
        )

    def test_initialisable(self):
        self._initialise()

    def test_request_client_token_returns_refreshing_token(self):
        cred = self._initialise()
        token = cred.request_client_token()
        self.assertIsInstance(token, RefreshingToken)

    def test_user_authorisation_url_equal_to_credentials(self):
        auth = Credentials(self.client_id, self.client_secret, self.redirect_uri)
        util = self._initialise()
        self.assertEqual(
            auth.user_authorisation_url(),
            util.user_authorisation_url()
        )
