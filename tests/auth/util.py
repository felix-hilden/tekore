from unittest.mock import MagicMock, patch

import pytest

from tekore import (
    RefreshingToken,
    UserAuth,
    parse_code_from_url,
    parse_state_from_url,
    prompt_for_pkce_token,
    prompt_for_user_token,
    refresh_pkce_token,
    refresh_user_token,
    request_client_token,
)


class TestParseCodeFromURL:
    def test_empty_url_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url("")

    def test_no_code_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url("http://example.com")

    def test_multiple_codes_raises(self):
        with pytest.raises(KeyError):
            parse_code_from_url("http://example.com?code=1&code=2")

    def test_single_code_returned(self):
        r = parse_code_from_url("http://example.com?code=1")
        assert r == "1"


class TestParseStateFromURL:
    def test_empty_url_raises(self):
        with pytest.raises(KeyError):
            parse_state_from_url("")

    def test_no_code_raises(self):
        with pytest.raises(KeyError):
            parse_state_from_url("http://example.com")

    def test_multiple_codes_raises(self):
        with pytest.raises(KeyError):
            parse_state_from_url("http://example.com?state=1&state=2")

    def test_single_code_returned(self):
        r = parse_state_from_url("http://example.com?state=1")
        assert r == "1"


def make_user_auth():
    cred = MagicMock()
    cred.request_user_token.return_value = "token"
    return UserAuth(cred, "scope")


class TestUserAuth:
    def test_repr(self):
        auth = make_user_auth()
        assert repr(auth).startswith("UserAuth(")

    def test_user_auth_correct_state(self):
        auth = make_user_auth()
        assert auth.request_token("code", auth.state)

    def test_user_auth_parse_from_url(self):
        auth = make_user_auth()
        url = f"http://redirect.com?code=code&state={auth.state}"
        assert auth.request_token(url=url) == "token"

    def test_user_auth_incorrect_state_raises(self):
        auth = make_user_auth()
        with pytest.raises(AssertionError):
            auth.request_token("code", "wrong-state")


class TestTokenUtilityFunctions:
    @pytest.mark.parametrize("open_browser", [True, False])
    def test_prompt_for_user_token(self, open_browser):
        cred = MagicMock()
        input_ = MagicMock(return_value="http://example.com?code=1&state=s")
        state = MagicMock(return_value="s")
        util_mod = "tekore._auth.util"
        with (
            patch("tekore._auth.refreshing.Credentials", cred),
            patch(util_mod + ".webbrowser", MagicMock()),
            patch(util_mod + ".input", input_),
            patch(util_mod + ".print", MagicMock()),
            patch(util_mod + ".gen_state", state),
        ):
            prompt_for_user_token("", "", "", open_browser)

        input_.assert_called_once()

    @pytest.mark.api
    def test_request_refreshed_token_returns_refreshing_token(
        self, app_env, user_refresh
    ):
        token = refresh_user_token(app_env[0], app_env[1], user_refresh)
        assert isinstance(token, RefreshingToken)
        token.credentials.close()

    @pytest.mark.api
    def test_expiring_user_token_refreshed(self, app_env, user_refresh):
        token = refresh_user_token(app_env[0], app_env[1], user_refresh)
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        assert old_token != str(token)
        token.credentials.close()

    @pytest.mark.api
    def test_request_client_token_returns_refreshing_token(self, app_env):
        token = request_client_token(app_env[0], app_env[1])
        assert isinstance(token, RefreshingToken)
        token.credentials.close()

    @pytest.mark.api
    def test_expiring_client_token_refreshed(self, app_env):
        token = request_client_token(app_env[0], app_env[1])
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        assert old_token != str(token)
        token.credentials.close()

    @pytest.mark.parametrize("open_browser", [True, False])
    def test_prompt_for_pkce_token(self, open_browser):
        cred = MagicMock()
        cred.pkce_user_authorisation.return_value = ("https://a.com", "verifier")
        cred_factory = MagicMock(return_value=cred)
        input_ = MagicMock(return_value="http://example.com?code=1&state=s")
        state = MagicMock(return_value="s")
        util_mod = "tekore._auth.util"
        with (
            patch("tekore._auth.refreshing.Credentials", cred_factory),
            patch(util_mod + ".webbrowser", MagicMock()),
            patch(util_mod + ".input", input_),
            patch(util_mod + ".print", MagicMock()),
            patch(util_mod + ".gen_state", state),
        ):
            prompt_for_pkce_token("", "", open_browser=open_browser)

        input_.assert_called_once()

    def test_request_refreshed_pkce_returns_refreshing_token(
        self, app_env, user_refresh
    ):
        cred = MagicMock()
        cred_factory = MagicMock(return_value=cred)
        with patch("tekore._auth.refreshing.Credentials", cred_factory):
            token = refresh_pkce_token(app_env[0], user_refresh)
        assert isinstance(token, RefreshingToken)
