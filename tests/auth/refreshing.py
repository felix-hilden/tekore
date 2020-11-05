from unittest.mock import MagicMock
from tekore import Token, Credentials, RefreshingToken, RefreshingCredentials


def make_token_obj(value: str, expiring: bool):
    """
    Make a token object.

    Args:
        value: (todo): write your description
        expiring: (str): write your description
    """
    token = MagicMock()
    token.is_expiring = expiring
    token.access_token = value
    return token


class TestRefreshingToken:
    def test_repr(self):
        """
        Test if the token has a valid token

        Args:
            self: (todo): write your description
        """
        low_token = make_token_obj('token', False)
        cred = MagicMock()

        auto_token = RefreshingToken(low_token, cred)
        assert repr(auto_token).startswith('RefreshingToken(')

    def test_fresh_token_returned(self):
        """
        Check if the token for the given token.

        Args:
            self: (todo): write your description
        """
        low_token = make_token_obj('token', False)
        cred = MagicMock()

        auto_token = RefreshingToken(low_token, cred)
        assert auto_token.access_token == 'token'

    def test_expiring_token_refreshed(self):
        """
        Test if a token is valid access token.

        Args:
            self: (todo): write your description
        """
        expiring = make_token_obj('expiring', True)
        refreshed = make_token_obj('refreshed', False)
        cred = MagicMock()
        cred.refresh.return_value = refreshed

        auto_token = RefreshingToken(expiring, cred)
        assert auto_token.access_token == 'refreshed'

    def test_refreshing_token_has_same_attributes_as_regular(self):
        """
        Test if a token attributes have a tokenized.

        Args:
            self: (todo): write your description
        """
        token_info = MagicMock()
        token = Token(token_info, uses_pkce=False)
        token._expires_at = 3000
        auto_token = RefreshingToken(token, MagicMock())

        token_attributes = [a for a in dir(token) if not a.startswith('_')]
        auto_attributes = [a for a in dir(auto_token) if not a.startswith('_')]

        for attribute in token_attributes:
            auto_token.__getattribute__(attribute)
            assert attribute in auto_attributes

    def test_refreshing_token_expiration_attributes(self):
        """
        Test if the token is expired : return : attr : token.

        Args:
            self: (todo): write your description
        """
        token_info = MagicMock()
        token = Token(token_info, uses_pkce=False)
        token._expires_at = 0

        auto_token = RefreshingToken(token, MagicMock())
        assert auto_token.is_expiring is False
        assert auto_token.expires_in is None
        assert auto_token.expires_at is None


class TestRefreshingCredentials:
    def test_repr(self):
        """
        Test if the test.

        Args:
            self: (todo): write your description
        """
        c = RefreshingCredentials('id', 'secret')
        assert repr(c).startswith('RefreshingCredentials(')

    def test_initialisable(self, app_env):
        """
        The initial initial setup.

        Args:
            self: (todo): write your description
            app_env: (todo): write your description
        """
        RefreshingCredentials(*app_env)

    def test_request_client_token_returns_refreshing_token(self, app_env):
        """
        Returns an oauth token.

        Args:
            self: (todo): write your description
            app_env: (todo): write your description
        """
        cred = RefreshingCredentials(*app_env)
        token = cred.request_client_token()
        assert isinstance(token, RefreshingToken)

    def test_user_authorisation_url_equal_to_expiring(self, app_env):
        """
        Test if user is_env_authoriring.

        Args:
            self: (todo): write your description
            app_env: (todo): write your description
        """
        auth = Credentials(*app_env)
        util = RefreshingCredentials(*app_env)
        assert auth.user_authorisation_url() == util.user_authorisation_url()
