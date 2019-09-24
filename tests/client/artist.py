from ._cred import TestCaseWithCredentials
from spotipy.client import SpotifyArtist


class TestSpotifyArtist(TestCaseWithCredentials):
    artist_id = '2SRIVGDkdqQnrQdaXxDkJt'
    artist_ids = [artist_id, '2aaLAng2L2aWD2FClzwiep']

    def setUp(self):
        self.client = SpotifyArtist(self.app_token)

    def test_artist(self):
        artist = self.client.artist(self.artist_id)
        self.assertEqual(artist.id, self.artist_id)

    def test_artists(self):
        artists = self.client.artists(self.artist_ids)
        self.assertEqual(len(artists), 2)

    def test_artist_albums_with_market(self):
        albums = self.client.artist_albums(self.artist_id, market='US')
        self.assertTrue(albums.total > 0)

    def test_artist_albums_no_market(self):
        albums = self.client.artist_albums(self.artist_id, market=None)
        self.assertTrue(albums.total > 0)

    def test_artist_top_tracks_with_country(self):
        tracks = self.client.artist_top_tracks(self.artist_id, country='US')
        self.assertTrue(len(tracks) > 0)

    def test_artist_top_tracks_no_country_raises(self):
        from requests.exceptions import HTTPError
        with self.assertRaises(HTTPError):
            self.client.artist_top_tracks(self.artist_id, country=None)

    def test_artist_related_artists(self):
        artists = self.client.artist_related_artists(self.artist_id)
        self.assertTrue(len(artists) > 0)
