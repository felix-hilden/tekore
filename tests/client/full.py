from unittest import TestCase
from unittest.mock import MagicMock

from ._cred import TestCaseWithUserCredentials
from ._resources import playlist_id
from spotipy.client import Spotify


class TestSpotifyBaseUnits(TestCase):
    def setUp(self):
        self.client = Spotify('token')

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


class TestSpotifyFull(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

    def test_search_paging_next(self):
        cat, = self.client.search('sheeran', limit=1)
        cat_next = self.client.next(cat)
        self.assertGreater(cat_next.total, 0)

    def test_search_paging_previous(self):
        cat, = self.client.search('sheeran', limit=1)
        cat_next = self.client.next(cat)
        cat_prev = self.client.previous(cat_next)
        self.assertEqual(cat.items[0].id, cat_prev.items[0].id)

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
