from ._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import album_id, album_ids

from spotipy.client import SpotifyAlbum


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
