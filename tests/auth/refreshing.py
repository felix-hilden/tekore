from unittest.mock import MagicMock
from tekore import Token, Credentials, RefreshingToken, RefreshingCredentials


def make_token_obj(value: str, expiring: bool):
    token = MagicMock()
    token.is_expiring = expiring
    token.access_token = value
    return token


class TestRefreshingToken:
    def test_fresh_token_returned(self):
        low_token = make_token_obj('token', False)
        cred = MagicMock()

        auto_token = RefreshingToken(low_token, cred)
        assert auto_token.access_token == 'token'

    def test_expiring_token_refreshed(self):
        expiring = make_token_obj('expiring', True)
        refreshed = make_token_obj('refreshed', False)
        cred = MagicMock()
        cred.refresh.return_value = refreshed

        auto_token = RefreshingToken(expiring, cred)
        assert auto_token.access_token == 'refreshed'

    def test_refreshing_token_has_same_attributes_as_regular(self):
        token_info = MagicMock()
        token = Token(token_info)
        token._expires_at = 3000
        auto_token = RefreshingToken(token, MagicMock())

        token_attributes = [a for a in dir(token) if not a.startswith('_')]
        auto_attributes = [a for a in dir(auto_token) if not a.startswith('_')]

        for attribute in token_attributes:
            auto_token.__getattribute__(attribute)
            assert attribute in auto_attributes

    def test_refreshing_token_expiration_attributes(self):
        token_info = MagicMock()
        token = Token(token_info)
        token._expires_at = 0

        auto_token = RefreshingToken(token, MagicMock())
        assert auto_token.is_expiring is False
        assert auto_token.expires_in is None
        assert auto_token.expires_at is None


class TestRefreshingCredentials:
    def test_initialisable(self, app_env):
        RefreshingCredentials(*app_env)

    def test_request_client_token_returns_refreshing_token(self, app_env):
        cred = RefreshingCredentials(*app_env)
        token = cred.request_client_token()
        assert isinstance(token, RefreshingToken)

    def test_user_authorisation_url_equal_to_expiring(self, app_env):
        auth = Credentials(*app_env)
        util = RefreshingCredentials(*app_env)
        assert auth.user_authorisation_url() == util.user_authorisation_url()
