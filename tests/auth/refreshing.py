from unittest import TestCase
from unittest.mock import MagicMock

from tekore import Token, Credentials, RefreshingToken, RefreshingCredentials
from tests._cred import TestCaseWithCredentials


def make_token_obj(value: str, expiring: bool):
    token = MagicMock()
    token.is_expiring = expiring
    token.access_token = value
    return token


class TestRefreshingToken(TestCase):
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
