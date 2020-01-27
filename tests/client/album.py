from tests._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import album_id, album_ids, album_relinked, album_restricted

from tekore.client.api import SpotifyAlbum


class TestSpotifyAlbum(TestCaseWithCredentials):
    def setUp(self):
        self.client = SpotifyAlbum(token=self.app_token)

    def test_album_with_market(self):
        album = self.client.album(album_id, market='US')
        self.assertEqual(album.id, album_id)

    def test_album_no_market(self):
        album = self.client.album(album_id, market=None)
        self.assertTrue(album.available_markets is not None)

    def test_album_tracks_with_market(self):
        self.client.album_tracks(album_id, market='US')

    def test_album_tracks_no_market(self):
        self.client.album_tracks(album_id, market=None)

    def test_album_tracks_relinking(self):
        tracks = self.client.album_tracks(album_relinked, market='US', limit=1)
        track = tracks.items[0]

        self.assertTrue(track.is_playable)

    def test_album_tracks_restricted(self):
        tracks = self.client.album_tracks(album_restricted, market='SE', limit=1)
        track = tracks.items[0]

        with self.subTest('Playable'):
            self.assertFalse(track.is_playable)
        with self.subTest('Restrictions'):
            self.assertEqual(track.restrictions.reason, 'market')

    def test_albums_with_market(self):
        albums = self.client.albums(album_ids, market='US')
        self.assertEqual(len(albums), len(album_ids))

    def test_albums_no_market(self):
        albums = self.client.albums(album_ids, market=None)
        self.assertEqual(len(albums), len(album_ids))


class TestSpotifyAlbumAsUser(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyAlbum(self.user_token)

    def test_album_from_token(self):
        album = self.client.album(album_id, market='from_token')
        self.assertEqual(album.id, album_id)

    def test_album_tracks_from_token(self):
        self.client.album_tracks(album_id, market='from_token')

    def test_albums_from_token(self):
        albums = self.client.albums(album_ids, market='from_token')
        self.assertEqual(len(albums), len(album_ids))
