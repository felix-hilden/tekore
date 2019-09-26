from ._cred import TestCaseWithCredentials
from ._resources import artist_id, artist_ids

from spotipy.client import SpotifyArtist


class TestSpotifyArtist(TestCaseWithCredentials):
    def setUp(self):
        self.client = SpotifyArtist(self.app_token)

    def test_artist(self):
        artist = self.client.artist(artist_id)
        self.assertEqual(artist.id, artist_id)

    def test_artists(self):
        artists = self.client.artists(artist_ids)
        self.assertEqual(len(artists), len(artist_ids))

    def test_artist_albums_with_market(self):
        albums = self.client.artist_albums(artist_id, market='US')
        self.assertTrue(albums.total > 0)

    def test_artist_albums_no_market(self):
        albums = self.client.artist_albums(artist_id, market=None)
        self.assertTrue(albums.total > 0)

    def test_artist_top_tracks_with_country(self):
        tracks = self.client.artist_top_tracks(artist_id, country='US')
        self.assertTrue(len(tracks) > 0)

    def test_artist_top_tracks_no_country_raises(self):
        from requests.exceptions import HTTPError
        with self.assertRaises(HTTPError):
            self.client.artist_top_tracks(artist_id, country=None)

    def test_artist_related_artists(self):
        artists = self.client.artist_related_artists(artist_id)
        self.assertTrue(len(artists) > 0)
