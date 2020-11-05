import pytest
from unittest.mock import MagicMock

from tekore import HTTPError
from tekore.model import PlayerErrorReason
from tekore import Spotify

from ._resources import album_id


@pytest.fixture
def client():
    """
    Returns a client.

    Args:
    """
    return Spotify('token')


class TestSpotifyBaseUnits:
    def test_repr(self):
        """
        Print a python version of the python version.

        Args:
            self: (todo): write your description
        """
        s = Spotify()
        assert repr(s).startswith('Spotify(')

    def test_token_is_given_token(self):
        """
        Check if the token is valid.

        Args:
            self: (todo): write your description
        """
        token = MagicMock()
        client = Spotify(token)
        assert token is client.token

    def test_token_assignable(self, client):
        """
        Assigns the client to be sent.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        client.token = 'new'
        assert client.token == 'new'

    def test_bad_request_is_parsed_for_error_reason(self, client):
        """
        Check if a bad bad bad bad bad bad request.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        error = list(PlayerErrorReason)[0]

        class BadResponse:
            status_code = 404
            url = 'example.com'
            content = {'error': {
                'message': 'Error message',
                'reason': error.name
            }}

        sender = MagicMock()
        sender.send.return_value = BadResponse()
        sender.is_async = False
        client.sender = sender

        try:
            client.album('not-an-id')
            raise AssertionError()
        except HTTPError as e:
            assert error.value in str(e)


class TestSpotifyBase:
    def test_album_nonexistent_market_error_message_parsed(self, app_client):
        """
        Test if an error message.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        try:
            app_client.album(album_id, market='__')
            raise AssertionError()
        except HTTPError as e:
            assert 'Invalid market code' in str(e)
