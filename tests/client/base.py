import unittest
from unittest.mock import MagicMock

from requests import HTTPError
from tekore.client import Spotify
from tekore.client.base import SpotifyBase
from tekore.model.error import PlayerErrorReason

from ._cred import TestCaseWithUserCredentials
from ._resources import album_id


class TestSpotifyBaseUnits(unittest.TestCase):
    def setUp(self):
        self.client = SpotifyBase('token')

    def test_token_is_given_token(self):
        token = MagicMock()
        client = SpotifyBase(token)
        self.assertIs(token, client.token)

    def test_token_assignable(self):
        self.client.token = 'new'
        self.assertEqual(self.client.token, 'new')

    def test_bad_request_is_parsed_for_error_reason(self):
        error = list(PlayerErrorReason)[0]

        class BadResponse:
            status_code = 404
            url = 'example.com'
            reason = 'Service not found!'

            @staticmethod
            def json():
                return {'error': {
                    'message': 'Error message',
                    'reason': error.name
                }}

        sender = MagicMock()
        sender.send.return_value = BadResponse()
        self.client.sender = sender

        try:
            self.client._get('example.com')
        except HTTPError as e:
            self.assertIn(error.value, str(e))


class TestSpotifyBase(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

    def test_album_nonexistent_market_error_message_parsed(self):
        try:
            self.client.album(album_id, market='__')
            self.assertTrue(False)
        except HTTPError as e:
            self.assertIn('Invalid market code', str(e))
