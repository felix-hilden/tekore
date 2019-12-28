import unittest
from unittest.mock import MagicMock, patch

from requests import HTTPError
from spotipy.auth import AccessToken, Token, Credentials, OAuthError, request_token


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


def make_token():
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

        with patch('spotipy.auth.time', time):
            token = Token(make_token())
            self.assertEqual(token.access_token, 'accesstoken')

    def test_expires_in_set_time(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch('spotipy.auth.time', time):
            token = Token(make_token())
            self.assertEqual(token.expires_in, 3600)

    def test_expires_in_is_refreshed(self):
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch('spotipy.auth.time', time):
            token = Token(make_token())
            self.assertEqual(token.expires_in, 3599)

    def test_old_token_is_expiring(self):
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch('spotipy.auth.time', time):
            token = Token(make_token())
            self.assertEqual(token.is_expiring, True)


class TestCredentials(unittest.TestCase):
    def test_credentials_takes_arguments(self):
        Credentials(client_id='id', client_secret='secret', redirect_uri='uri')

    def test_request_token(self):
        response = MagicMock()
        response.status_code = 200

        post_mock = MagicMock(return_value=response)
        with patch('spotipy.auth.post', post_mock):
            request_token('auth', {})
            post_mock.assert_called_once()

    def test_bad_code_raises_oauth_error(self):
        response = MagicMock()
        response.status_code = 400

        post_mock = MagicMock(return_value=response)
        with patch('spotipy.auth.post', post_mock):
            with self.assertRaises(OAuthError):
                request_token('auth', {})

    def test_server_error_raises_http_error(self):
        response = MagicMock()
        response.status_code = 500

        post_mock = MagicMock(return_value=response)
        with patch('spotipy.auth.post', post_mock):
            with self.assertRaises(HTTPError):
                request_token('auth', {})

    def test_request_client_token(self):
        c = Credentials('id', 'secret', 'uri')
        mock = MagicMock()
        with patch('spotipy.auth.request_token', mock):
            c.request_client_token()
            mock.assert_called_once()

    def test_user_authorisation_url(self):
        c = Credentials('id', 'secret', 'uri')
        url = c.user_authorisation_url('scope', 'state', True)
        self.assertIn('scope=scope', url)
        self.assertIn('state=state', url)
        self.assertIn('show_dialog=true', url)

    def test_request_user_token(self):
        c = Credentials('id', 'secret', 'uri')
        mock = MagicMock()
        with patch('spotipy.auth.request_token', mock):
            c.request_user_token('code')
            mock.assert_called_once()

    def test_request_refreshed_token(self):
        c = Credentials('id', 'secret', 'uri')
        request_token_mock = MagicMock(return_value=MagicMock())
        with patch('spotipy.auth.request_token', request_token_mock):
            c.refresh_user_token('refresh')

    def test_request_refreshed_token_uses_old_if_not_returned(self):
        c = Credentials('id', 'secret', 'uri')
        new = MagicMock()
        new.refresh_token = None

        request_token_mock = MagicMock(return_value=new)
        with patch('spotipy.auth.request_token', request_token_mock):
            refreshed = c.refresh_user_token('refresh')
            self.assertEqual(refreshed.refresh_token, 'refresh')

    def test_refresh_wraps_token_refresh_token(self):
        token = MagicMock()
        token.refresh_token = 'refresh'

        new = MagicMock()
        mock = MagicMock(return_value=new)
        with patch('spotipy.auth.Credentials.refresh_user_token', mock):
            c = Credentials('id', 'secret', 'uri')
            refreshed = c.refresh(token)
            with self.subTest('Refresh token extracted'):
                mock.assert_called_with('refresh')
            with self.subTest('Refreshed token returned as is'):
                self.assertIs(refreshed, new)
