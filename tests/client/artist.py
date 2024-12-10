import pytest

from tekore.model import AlbumGroup

from ._resources import artist_id, artist_ids


@pytest.mark.api
class TestSpotifyArtist:
    def test_artist(self, app_client):
        artist = app_client.artist(artist_id)
        assert artist.id == artist_id

    def test_artists(self, app_client):
        artists = app_client.artists(artist_ids)
        assert len(artists) == len(artist_ids)

    def test_artist_albums_with_market(self, app_client):
        albums = app_client.artist_albums(artist_id, market="US")
        assert albums.total > 0

    def test_artist_albums_no_market(self, app_client):
        albums = app_client.artist_albums(artist_id, market=None)
        assert albums.total > 0

    def test_artist_albums_groups(self, app_client):
        albums = app_client.artist_albums(
            artist_id,
            include_groups=[AlbumGroup.album, AlbumGroup.compilation],
            market=None,
        )
        assert albums.total > 0

    @pytest.mark.xfail(reason="Consistent unexpected failures in CI")
    def test_artist_albums_no_groups_returns_all(self, app_client):
        albums = app_client.artist_albums(artist_id, include_groups=[], market=None)
        assert albums.total > 0

    def test_artist_top_tracks_with_country(self, app_client):
        tracks = app_client.artist_top_tracks(artist_id, market="US")
        assert len(tracks) > 0

    def test_artist_related_artists(self, app_client):
        artists = app_client.artist_related_artists(artist_id)
        assert len(artists) > 0

    def test_artist_albums_from_token(self, user_client):
        albums = user_client.artist_albums(artist_id, market="from_token")
        assert albums.total > 0

    def test_artist_top_tracks_from_token(self, user_client):
        tracks = user_client.artist_top_tracks(artist_id, market="from_token")
        assert len(tracks) > 0
