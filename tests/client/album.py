from ._cred import TestCaseWithCredentials
from spotipy.client import SpotifyAlbum


class TestSpotifyAlbum(TestCaseWithCredentials):
    album_id = '3RBULTZJ97bvVzZLpxcB0j'
    album_ids = [album_id, '7khFXQNBzcfSfgGjPKerdE']

    def setUp(self):
        self.client = SpotifyAlbum(token=self.app_token)

    def test_album_with_market(self):
        album = self.client.album(self.album_id, market='US')
        self.assertEqual(album.id, self.album_id)

    def test_album_no_market(self):
        album = self.client.album(self.album_id, market=None)
        self.assertTrue(album.available_markets is not None)

    def test_album_tracks_with_market(self):
        tracks = self.client.album_tracks(self.album_id, market='US')
        self.assertEqual(tracks.total, 11)

    def test_album_tracks_no_market(self):
        tracks = self.client.album_tracks(self.album_id, market=None)
        self.assertEqual(tracks.total, 11)

    def test_albums_with_market(self):
        albums = self.client.albums(self.album_ids, market='US')
        self.assertEqual(len(albums), 2)

    def test_albums_no_market(self):
        albums = self.client.albums(self.album_ids, market=None)
        self.assertEqual(len(albums), 2)
