import unittest
from unittest.mock import MagicMock, patch
from tests.client._cred import TestCaseWithCredentials, TestCaseWithUserCredentials

from spotipy.auth import Token, Credentials
from spotipy.util import (
    RefreshingToken,
    parse_code_from_url,
    prompt_for_user_token,
    credentials_from_environment,
    refresh_user_token,
    request_client_token,
    RefreshingCredentials,
)


def make_token(value: str, expiring: bool):
    token = MagicMock()
    token.is_expiring = expiring
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
        token.expires_at = 0

        auto_token = RefreshingToken(token, MagicMock())
        with self.subTest('is_expiring is False'):
            self.assertFalse(auto_token.is_expiring)
        with self.subTest('expires_in is None'):
            self.assertIsNone(auto_token.expires_in)
        with self.subTest('expires_at is None'):
            self.assertIsNone(auto_token.expires_at)


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


class TestTokenUtilityFunctions(TestCaseWithUserCredentials):
    def test_prompt_for_user_token(self):
        cred = MagicMock()
        cred.authorisation_url.return_value = 'http://example.com'
        cred.request_access_token.return_value = MagicMock()
        input_ = MagicMock(return_value='http://example.com?code=1')
        with patch('spotipy.util.Credentials', cred),\
                patch('spotipy.util.webbrowser', MagicMock()),\
                patch('spotipy.util.input', input_),\
                patch('spotipy.util.print', MagicMock()):
            token = prompt_for_user_token('', '', '')

        with self.subTest('Input prompted'):
            input_.assert_called_once()

        with self.subTest('Refreshing token returned'):
            self.assertIsInstance(token, RefreshingToken)

    def test_request_refreshed_token_returns_refreshing_token(self):
        token = refresh_user_token(
            self.client_id,
            self.client_secret,
            self.user_token.refresh_token
        )
        self.assertIsInstance(token, RefreshingToken)

    def test_expiring_user_token_refreshed(self):
        token = refresh_user_token(
            self.client_id,
            self.client_secret,
            self.user_token.refresh_token
        )
        old_token = str(token)
        token._token.expires_at -= token._token.expires_in - 30
        self.assertNotEqual(old_token, str(token))

    def test_request_client_token_returns_refreshing_token(self):
        token = request_client_token(
            self.client_id,
            self.client_secret
        )
        self.assertIsInstance(token, RefreshingToken)

    def test_expiring_client_token_refreshed(self):
        token = request_client_token(
            self.client_id,
            self.client_secret
        )
        old_token = str(token)
        token._token.expires_at -= token._token.expires_in - 30
        self.assertNotEqual(old_token, str(token))


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


if __name__ == '__main__':
    unittest.main()
