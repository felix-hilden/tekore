import pytest

from tekore import HTTPError

from ._resources import (
    album_id,
    track_id,
    track_ids,
    track_no_audio_features,
    track_relinked,
    track_restricted,
)


@pytest.mark.api
class TestSpotifyTrack:
    def test_track_with_market(self, app_client):
        track = app_client.track(track_id, market="US")
        assert track.id == track_id
        assert track.available_markets is None
        assert track.is_playable is not None

    def test_track_no_market(self, app_client):
        track = app_client.track(track_id, market=None)
        assert track.id == track_id
        assert len(track.available_markets) > 0
        assert track.is_playable is None

    def test_track_restricted(self, app_client):
        track = app_client.track(track_restricted, market="SE")

        assert track.is_playable is False
        assert track.restrictions.reason == "market"

    @pytest.mark.skipif(not track_relinked, reason="No known relinked track")
    def test_track_relinking(self, app_client):
        track = app_client.track(track_relinked, market="US")

        assert track_relinked != track.id
        assert track_relinked == track.linked_from.id
        assert track.is_playable is True

    def test_tracks_with_market(self, app_client):
        tracks = app_client.tracks(track_ids, market="US")
        assert len(tracks) == len(track_ids)
        assert all(track.available_markets is None for track in tracks)
        assert all(track.is_playable is not None for track in tracks)

    def test_tracks_no_market(self, app_client):
        tracks = app_client.tracks(track_ids, market=None)
        assert len(tracks) == len(track_ids)
        assert all(len(track.available_markets) > 0 for track in tracks)
        assert all(track.is_playable is None for track in tracks)

    def test_simple_tracks_with_market(self, app_client):
        tracks = app_client.album(album_id, market="US").tracks.items
        assert all(track.available_markets is None for track in tracks)
        assert all(track.is_playable is not None for track in tracks)

    def test_simple_tracks_no_market(self, app_client):
        tracks = app_client.album(album_id, market=None).tracks.items
        assert all(len(track.available_markets) > 0 for track in tracks)
        assert all(track.is_playable is None for track in tracks)

    def test_track_audio_analysis(self, app_client):
        app_client.track_audio_analysis(track_id)

    def test_track_audio_features(self, app_client):
        features = app_client.track_audio_features(track_id)
        assert features.id == track_id

    def test_tracks_audio_features(self, app_client):
        features = app_client.tracks_audio_features(track_ids)
        assert [f.id for f in features] == track_ids

    @pytest.mark.skipif(
        not track_no_audio_features, reason="No known track without audio features"
    )
    def test_track_audio_features_not_found_raises(self, app_client):
        with pytest.raises(HTTPError):
            app_client.track_audio_features(track_no_audio_features)

    @pytest.mark.skipif(
        not track_no_audio_features, reason="No known track without audio features"
    )
    def test_tracks_audio_features_not_found_is_none(self, app_client):
        features = app_client.tracks_audio_features([track_no_audio_features])
        assert features[0] is None

    def test_track_from_token(self, user_client):
        track = user_client.track(track_id, market="from_token")
        assert track.id == track_id

    def test_tracks_from_token(self, user_client):
        tracks = user_client.tracks(track_ids, market="from_token")
        assert len(tracks) == len(track_ids)
