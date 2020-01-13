from ._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import artist_id, artist_ids

from tekore.client.api import SpotifyArtist
from tekore.model import AlbumGroup


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
        self.assertGreater(albums.total, 0)

    def test_artist_albums_no_market(self):
        albums = self.client.artist_albums(artist_id, market=None)
        self.assertGreater(albums.total, 0)

    def test_artist_albums_groups(self):
        albums = self.client.artist_albums(
            artist_id,
            include_groups=[AlbumGroup.album, AlbumGroup.compilation],
            market=None
        )
        self.assertGreater(albums.total, 0)

    def test_artist_albums_no_groups_returns_empty(self):
        albums = self.client.artist_albums(
            artist_id,
            include_groups=[],
            market=None
        )
        self.assertEqual(albums.total, 0)

    def test_artist_top_tracks_with_country(self):
        tracks = self.client.artist_top_tracks(artist_id, market='US')
        self.assertGreater(len(tracks), 0)

    def test_artist_related_artists(self):
        artists = self.client.artist_related_artists(artist_id)
        self.assertGreater(len(artists), 0)


class TestSpotifyArtistAsUser(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyArtist(self.user_token)

    def test_artist_albums_from_token(self):
        albums = self.client.artist_albums(artist_id, market='from_token')
        self.assertGreater(albums.total, 0)

    def test_artist_top_tracks_from_token(self):
        tracks = self.client.artist_top_tracks(artist_id, market='from_token')
        self.assertGreater(len(tracks), 0)
