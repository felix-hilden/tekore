from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tekore import AccessToken, Credentials, HTTPError, Response, Scope, Token


class TestAccessToken:
    def test_access_token_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            AccessToken()

    def test_str_of_access_token_is_value_of_property(self):
        class T(AccessToken):
            @property
            def access_token(self):
                return "token"

        t = T()
        assert t.access_token == str(t)


def token_dict():
    return {
        "access_token": "accesstoken",
        "expires_in": 3600,
        "token_type": "tokentype",
        "scope": "space separated list",
        "refresh_token": "refreshtoken",
    }


def make_token(attrs: dict | None = None, *, uses_pkce: bool = False):
    a = token_dict()
    a.update(attrs or {})
    return Token(a, uses_pkce)


time_module = "tekore._auth.expiring.token.time"


class TestToken:
    def test_repr(self):
        t = make_token()
        assert repr(t).startswith("Token(")

    def test_access_token_returned(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(time_module, time):
            token = make_token()
            assert token.access_token == "accesstoken"

    def test_expires_in_set_time(self):
        time = MagicMock()
        time.time.return_value = 0

        with patch(time_module, time):
            token = make_token()
            assert token.expires_in == 3600

    def test_expires_in_is_refreshed(self):
        time = MagicMock()
        time.time.side_effect = [0, 1]

        with patch(time_module, time):
            token = make_token()
            assert token.expires_in == 3599

    def test_old_token_is_expiring(self):
        time = MagicMock()
        time.time.side_effect = [0, 3600]

        with patch(time_module, time):
            token = make_token()
            assert token.is_expiring is True

    def test_token_type(self):
        t = make_token()
        assert isinstance(t.token_type, str)

    def test_scope_parsed(self):
        t = make_token()
        assert isinstance(t.scope, Scope)

    def test_no_scope_is_empty(self):
        t = make_token({"scope": ""})
        assert len(t.scope) == 0


def mock_response(code: int = 200, content: dict | None = None) -> Response:
    return Response("https://url.com", {}, code, content or token_dict())


@pytest.mark.api
class TestCredentialsOnline:
    def test_request_client_token(self, app_env):
        c = Credentials(app_env[0], app_env[1])
        token = c.request_client_token()
        assert token.refresh_token is None
        assert str(token.scope) == ""
        c.close()

    @pytest.mark.asyncio
    async def test_async_request_client_token(self, app_env):
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.request_client_token()
        assert token.refresh_token is None
        assert str(token.scope) == ""
        await c.close()

    def test_refresh_user_token(self, app_env, user_refresh):
        c = Credentials(app_env[0], app_env[1])
        token = c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None
        assert len(token.scope) > 0
        c.close()

    @pytest.mark.asyncio
    async def test_async_refresh_user_token(self, app_env, user_refresh):
        c = Credentials(app_env[0], app_env[1], asynchronous=True)
        token = await c.refresh_user_token(user_refresh)
        assert token.refresh_token is not None
        assert len(token.scope) > 0
        await c.close()

    def test_bad_arguments_raises_error(self):
        c = Credentials("id", "secret")

        with pytest.raises(HTTPError):
            c.request_client_token()
        c.close()


cred_module = "tekore._auth.expiring.Credentials"


class TestCredentialsOffline:
    def test_repr(self):
        c = Credentials("id", "secret")
        assert repr(c).startswith("Credentials(")
        c.close()

    def test_credentials_initialisation(self):
        Credentials(client_id="id", client_secret="secret", redirect_uri="uri").close()  # noqa: S106

    def test_credentials_only_client_id_mandatory(self):
        Credentials("id").close()

    def test_basic_token_with_no_secret_raises(self):
        c = Credentials("id")
        with pytest.raises(ValueError, match="client secret is required"):
            c.request_client_token()
        c.close()

    def test_server_error_raises_http_error(self):
        c = Credentials("id", "secret")
        response = mock_response(500, {})
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()
        c.close()

    def test_client_error_with_description(self):
        c = Credentials("id", "secret")
        error = {"error": "Bad thing", "error_description": "because reasons"}
        response = mock_response(400, error)
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()
        c.close()

    def test_client_error_without_description(self):
        c = Credentials("id", "secret")
        error = {"error": "Bad thing"}
        response = mock_response(400, error)
        c.send = MagicMock(return_value=response)
        with pytest.raises(HTTPError):
            c.request_client_token()
        c.close()

    def test_user_authorisation_url(self):
        c = Credentials("id", redirect_uri="uri")
        url = c.user_authorisation_url("scope", "state")
        assert "scope=scope" in url
        assert "state=state" in url
        c.close()

    def test_user_authorisation_accepts_scope_list(self):
        c = Credentials("id", redirect_uri="uri")
        url = c.user_authorisation_url(["a", "b"], "state")
        assert "scope=a+b" in url
        c.close()

    def test_request_user_token(self):
        c = Credentials("id", "secret", "uri")
        send = MagicMock(return_value=mock_response())
        with patch(cred_module + ".send", send):
            c.request_user_token("code")
            send.assert_called_once()
        c.close()

    def test_refresh_user_token_uses_old_refresh_if_not_returned(self):
        c = Credentials("id", "secret")
        token = token_dict()
        token["refresh_token"] = None
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(cred_module + ".send", send):
            refreshed = c.refresh_user_token("refresh")
            assert refreshed.refresh_token == "refresh"
        c.close()

    def test_refresh_user_token_refresh_replaced_if_returned(self):
        c = Credentials("id", "secret")
        token = token_dict()
        response = mock_response(content=token)

        send = MagicMock(return_value=response)
        with patch(cred_module + ".send", send):
            refreshed = c.refresh_user_token("refresh")
            assert refreshed.refresh_token == token["refresh_token"]
        c.close()

    def test_pkce_user_authorisation(self):
        c = Credentials("id", redirect_uri="redirect")
        c.pkce_user_authorisation("scope", "state")
        c.close()

    def test_pkce_user_authorisation_invalid_verify_bytes(self):
        c = Credentials("id", redirect_uri="redirect")
        with pytest.raises(AssertionError):
            c.pkce_user_authorisation("scope", "state", verifier_bytes=1)
        c.close()

    def test_request_pkce_token(self):
        c = Credentials("id")
        c.send = MagicMock(return_value=mock_response())
        token = c.request_pkce_token("scope", "verifier")
        assert token.uses_pkce
        c.close()

    def test_refresh_pkce_token(self):
        c = Credentials("id")
        c.send = MagicMock(return_value=mock_response())
        token = c.refresh_pkce_token("refresh")
        assert token.uses_pkce
        c.close()

    def test_auto_refresh_client_token(self):
        c = Credentials("id", "secret")
        token = make_token({"refresh_token": None})
        c.request_client_token = MagicMock(return_value=token)
        c.refresh(token)
        c.request_client_token.assert_called_once()
        c.close()

    def test_auto_refresh_user_token(self):
        c = Credentials("id", "secret")
        token = make_token(uses_pkce=False)
        c.refresh_user_token = MagicMock(return_value=token)
        c.refresh(token)
        c.refresh_user_token.assert_called_once()
        c.close()

    def test_auto_refresh_pkce_token(self):
        c = Credentials("id")
        token = make_token(uses_pkce=True)
        c.refresh_pkce_token = MagicMock(return_value=token)
        c.refresh(token)
        c.refresh_pkce_token.assert_called_once()
        c.close()
