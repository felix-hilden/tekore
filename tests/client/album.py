import pytest

from ._resources import album_id, album_ids, album_relinked, album_restricted


@pytest.mark.api
class TestSpotifyAlbum:
    def test_album_with_market(self, app_client):
        album = app_client.album(album_id, market="US")
        assert album.id == album_id

    def test_album_no_market(self, app_client):
        album = app_client.album(album_id, market=None)
        assert album.available_markets is not None

    def test_album_tracks_with_market(self, app_client):
        tracks = app_client.album_tracks(album_id, market="US")
        assert tracks.total > 0

    def test_album_tracks_no_market(self, app_client):
        tracks = app_client.album_tracks(album_id, market=None)
        assert tracks.total > 0

    @pytest.mark.skipif(not album_relinked, reason="No known relinked album")
    def test_album_tracks_relinking(self, app_client):
        tracks = app_client.album_tracks(album_relinked, market="US", limit=1)
        track = tracks.items[0]
        assert track.linked_from is not None

    def test_album_tracks_restricted(self, app_client):
        tracks = app_client.album_tracks(album_restricted, market="SE", limit=1)
        track = tracks.items[0]

        assert track.is_playable is False
        assert track.restrictions.reason == "market"

    def test_albums_with_market(self, app_client):
        albums = app_client.albums(album_ids, market="US")
        assert len(albums) == len(album_ids)

    def test_albums_no_market(self, app_client):
        albums = app_client.albums(album_ids, market=None)
        assert len(albums) == len(album_ids)

    def test_album_from_token(self, user_client):
        album = user_client.album(album_id, market="from_token")
        assert album.id == album_id

    def test_album_tracks_from_token(self, user_client):
        tracks = user_client.album_tracks(album_id, market="from_token")
        assert tracks.total > 0

    def test_albums_from_token(self, user_client):
        albums = user_client.albums(album_ids, market="from_token")
        assert len(albums) == len(album_ids)
