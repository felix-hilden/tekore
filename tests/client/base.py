from unittest.mock import MagicMock

import pytest

from tekore import HTTPError, Response, Spotify
from tekore.model import PlayerErrorReason

from ._resources import album_id


@pytest.fixture
def client():
    return Spotify("token")


class TestSpotifyBaseUnits:
    def test_repr(self):
        s = Spotify()
        assert repr(s).startswith("Spotify(")

    def test_token_is_given_token(self):
        token = MagicMock()
        client = Spotify(token)
        assert token is client.token

    def test_token_assignable(self, client):
        client.token = "new"
        assert client.token == "new"

    def test_bad_request_is_parsed_for_error_reason(self, client):
        error = next(iter(PlayerErrorReason))
        response = Response(
            url="example.com",
            headers={},
            status_code=404,
            content={"error": {"message": "Error message", "reason": error.name}},
        )
        sender = MagicMock()
        sender.send.return_value = response
        sender.is_async = False
        client.sender = sender

        with pytest.raises(HTTPError, match=error.value):
            client.album("not-an-id")


@pytest.mark.api
class TestSpotifyBase:
    def test_album_nonexistent_market_error_message_parsed(self, app_client):
        with pytest.raises(HTTPError, match="__"):
            app_client.album(album_id, market="__")
