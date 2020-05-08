import pytest
from unittest.mock import MagicMock, patch

from tekore import (
    RefreshingToken,
    parse_code_from_url,
    prompt_for_user_token,
    refresh_user_token,
    request_client_token,
)


class TestParseCodeFromURL:
    def test_empty_url_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url('')

    def test_no_code_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url('http://example.com')

    def test_multiple_codes_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url('http://example.com?code=1&code=2')

    def test_single_code_returned(self):
        r = parse_code_from_url('http://example.com?code=1')
        assert r == '1'


class TestTokenUtilityFunctions:
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

        input_.assert_called_once()
        assert isinstance(token, RefreshingToken)

    def test_request_refreshed_token_returns_refreshing_token(
            self, app_env, user_refresh
    ):
        token = refresh_user_token(
            app_env[0],
            app_env[1],
            user_refresh
        )
        assert isinstance(token, RefreshingToken)

    def test_expiring_user_token_refreshed(self, app_env, user_refresh):
        token = refresh_user_token(
            app_env[0],
            app_env[1],
            user_refresh
        )
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        assert old_token != str(token)

    def test_request_client_token_returns_refreshing_token(self, app_env):
        token = request_client_token(app_env[0], app_env[1])
        assert isinstance(token, RefreshingToken)

    def test_expiring_client_token_refreshed(self, app_env):
        token = request_client_token(app_env[0], app_env[1])
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        assert old_token != str(token)
