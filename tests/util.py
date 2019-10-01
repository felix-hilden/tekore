import unittest
from unittest.mock import MagicMock, patch

from spotipy.auth import Token
from spotipy.util import (
    RefreshingToken,
    parse_code_from_url,
    prompt_for_user_token,
    credentials_from_environment,
    token_from_refresh_token,
)


def make_token(value: str, expiring: bool):
    token = MagicMock()
    token.is_expiring.return_value = expiring
    token.access_token = value
    return token


class TestRefreshingToken(unittest.TestCase):
    def test_fresh_token_returned(self):
        low_token = make_token('token', False)
        cred = MagicMock()

        auto_token = RefreshingToken(low_token, cred)
        self.assertEqual(auto_token.access_token, 'token')

    def test_expiring_token_refreshed(self):
        expiring = make_token('expiring', True)
        refreshed = make_token('refreshed', False)
        cred = MagicMock()
        cred.refresh.return_value = refreshed

        auto_token = RefreshingToken(expiring, cred)
        self.assertEqual(auto_token.access_token, 'refreshed')

    def test_refreshing_token_has_same_attributes_as_regular(self):
        token_info = MagicMock()
        token = Token(token_info)
        token.expires_at = 3000
        cred = MagicMock()
        auto_token = RefreshingToken(token, cred)

        token_attributes = [a for a in dir(token) if not a.startswith('_')]
        auto_attributes = [a for a in dir(auto_token) if not a.startswith('_')]

        for attribute in token_attributes:
            with self.subTest(f'Attribute: `{attribute}`'):
                auto_token.__getattribute__(attribute)
                self.assertTrue(attribute in auto_attributes)


class TestCredentialsFromEnvironment(unittest.TestCase):
    def test_environment_read_according_to_specified_names(self):
        import os
        id_name = 'SP_client_id'
        secret_name = 'SP_client_secret'
        uri_name = 'SP_redirect_uri'
        os.environ[id_name] = 'id'
        os.environ[secret_name] = 'secret'
        os.environ[uri_name] = 'uri'

        id_, secret, uri = credentials_from_environment(
            client_id_var=id_name,
            client_secret_var=secret_name,
            redirect_uri_var=uri_name
        )

        with self.subTest('Client ID'):
            self.assertEqual(id_, 'id')
        with self.subTest('Client secret'):
            self.assertEqual(secret, 'secret')
        with self.subTest('Redirect URI'):
            self.assertEqual(uri, 'uri')


class TestParseCodeFromURL(unittest.TestCase):
    def test_empty_url_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('')

    def test_no_code_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('http://example.com')

    def test_multiple_codes_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('http://example.com?code=1&code=2')

    def test_single_code_returned(self):
        r = parse_code_from_url('http://example.com?code=1')
        self.assertEqual(r, '1')


class TestPromptForToken(unittest.TestCase):
    def test_user_prompted_for_input(self):
        cred = MagicMock()
        cred.authorisation_url.return_value = 'http://example.com'
        cred.request_access_token.return_value = MagicMock()
        input_ = MagicMock(return_value='http://example.com?code=1')
        with patch('spotipy.util.Credentials', cred),\
                patch('spotipy.util.webbrowser', MagicMock()),\
                patch('spotipy.util.input', input_),\
                patch('spotipy.util.print', MagicMock()):
            prompt_for_user_token('', '', '')
            input_.assert_called_once()

    def test_refreshing_token_returned(self):
        cred = MagicMock()
        cred.authorisation_url.return_value = 'http://example.com'
        cred.request_access_token.return_value = MagicMock()
        input_ = MagicMock(return_value='http://example.com?code=1')
        with patch('spotipy.util.Credentials', cred),\
                patch('spotipy.util.webbrowser', MagicMock()),\
                patch('spotipy.util.input', input_),\
                patch('spotipy.util.print', MagicMock()):
            token = prompt_for_user_token('', '', '')
            self.assertIsInstance(token, RefreshingToken)


class TestTokenFromRefreshToken(unittest.TestCase):
    def test_request_refreshed_token_called(self):
        cred_instance = MagicMock()
        cred = MagicMock(return_value=cred_instance)
        cred_instance.request_refreshed_token.return_value = MagicMock()

        with patch('spotipy.util.Credentials', cred):
            token_from_refresh_token('', '', '', 'refresh')
            cred_instance.request_refreshed_token.assert_called_with('refresh')


if __name__ == '__main__':
    unittest.main()
