from ._cred import TestCaseWithUserCredentials
from ._resources import playlist_id

from spotipy.client import Spotify


class TestSpotifyPaging(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

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
