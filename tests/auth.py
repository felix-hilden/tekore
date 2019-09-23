import unittest
from unittest.mock import MagicMock, patch

from spotipy.auth import AccessToken, Token


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
            self.assertEqual(token.is_expiring(), True)
