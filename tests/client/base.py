import unittest
from unittest.mock import MagicMock

from requests import HTTPError
from spotipy.client import Spotify
from spotipy.client.base import SpotifyBase
from spotipy.model.error import PlayerErrorReason

from ._cred import TestCaseWithUserCredentials
from ._resources import album_id, playlist_id


class TestSpotifyBaseUnits(unittest.TestCase):
    def setUp(self):
        self.client = SpotifyBase('token')

    def test_token_equals_given_token(self):
        self.assertEqual(self.client.token, 'token')

    def test_token_assignable(self):
        self.client.token = 'new'
        self.assertEqual(self.client.token, 'new')

    def test_token_equals_str_of_given_value(self):
        self.client.token = 1
        self.assertEqual(self.client.token, '1')

    def test_new_token_used_in_context(self):
        with self.client.token_as('new'):
            self.assertEqual(self.client.token, 'new')

    def test_old_token_restored_after_context(self):
        with self.client.token_as('new'):
            pass
        self.assertEqual(self.client.token, 'token')

    def test_next_with_no_next_set_returns_none(self):
        paging = MagicMock()
        paging.next = None

        next_ = self.client.next(paging)
        self.assertIsNone(next_)

    def test_previous_with_no_previous_set_returns_none(self):
        paging = MagicMock()
        paging.previous = None

        previous = self.client.previous(paging)
        self.assertIsNone(previous)

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

    def test_followed_artists_paging_exhaust(self):
        artists = self.client.followed_artists()
        pages = list(self.client.all_pages(artists))
        self.assertIsNone(pages[-1].next)

    def test_recently_played_paging_exhaust(self):
        played = self.client.playback_recently_played()
        pages = list(self.client.all_pages(played))

        with self.subTest('Next is None'):
            self.assertIsNone(pages[-1].next)
        with self.subTest('Cursors is None'):
            self.assertIsNone(pages[-1].cursors)

    def test_all_pages_from_cursor_paging(self):
        played = self.client.playback_recently_played()
        pages = self.client.all_pages(played)
        self.assertTrue(all(isinstance(p, type(played)) for p in pages))

    def test_all_items_from_cursor_paging(self):
        played = self.client.playback_recently_played()
        items = self.client.all_items(played)
        self.assertTrue(all(isinstance(i, type(played.items[0])) for i in items))

    def test_all_pages_from_offset_paging(self):
        tracks = self.client.playlist_tracks(playlist_id, limit=20)
        pages = self.client.all_pages(tracks)
        self.assertTrue(all(isinstance(p, type(tracks)) for p in pages))

    def test_all_items_from_offset_paging(self):
        tracks = self.client.playlist_tracks(playlist_id, limit=20)
        items = self.client.all_items(tracks)
        self.assertTrue(all(isinstance(i, type(tracks.items[0])) for i in items))
