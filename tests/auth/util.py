import unittest
from unittest.mock import MagicMock, patch

from tekore import (
    RefreshingToken,
    parse_code_from_url,
    prompt_for_user_token,
    refresh_user_token,
    request_client_token,
)

from tests._cred import TestCaseWithUserCredentials


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
        with patch('tekore._auth.refreshing.Credentials', cred),\
                patch('tekore._auth.util.webbrowser', MagicMock()),\
                patch('tekore._auth.util.input', input_),\
                patch('tekore._auth.util.print', MagicMock()):
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
        token._token._expires_at -= token._token.expires_in - 30
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
        token._token._expires_at -= token._token.expires_in - 30
        self.assertNotEqual(old_token, str(token))
