import pytest
from ._resources import (
    track_id,
    track_ids,
    track_relinked,
    track_restricted,
    track_no_audio_features,
)
from tekore import HTTPError


class TestSpotifyTrack:
    def test_track_with_market(self, app_client):
        track = app_client.track(track_id, market='US')
        assert track.id == track_id

    def test_track_with_market_available_markets_not_in_response(self, app_client):
        track = app_client.track(track_id, market='US')
        assert track.available_markets is None

    def test_track_no_market(self, app_client):
        track = app_client.track(track_id, market=None)
        assert track.id == track_id

    def test_track_no_market_is_playable_not_in_response(self, app_client):
        track = app_client.track(track_id, market=None)
        assert track.is_playable is None

    def test_track_restricted(self, app_client):
        track = app_client.track(track_restricted, market='SE')

        assert track.is_playable is False
        assert track.restrictions.reason == 'market'

    def test_track_relinking(self, app_client):
        track = app_client.track(track_relinked, market='US')

        assert track_relinked != track.id
        assert track_relinked == track.linked_from.id
        assert track.is_playable is True

    def test_track_doesnt_have_episode_or_track(self, app_client):
        track = app_client.track(track_id)
        assert all(i is None for i in (track.episode, track.track))

    def test_tracks_with_market(self, app_client):
        tracks = app_client.tracks(track_ids, market='US')
        assert len(tracks) == len(track_ids)

    def test_tracks_no_market(self, app_client):
        tracks = app_client.tracks(track_ids, market=None)
        assert len(tracks) == len(track_ids)

    def test_track_audio_analysis(self, app_client):
        app_client.track_audio_analysis(track_id)

    def test_track_audio_features(self, app_client):
        features = app_client.track_audio_features(track_id)
        assert features.id == track_id

    def test_tracks_audio_features(self, app_client):
        features = app_client.tracks_audio_features(track_ids)
        assert [f.id for f in features] == track_ids

    @pytest.mark.skipif(
        not track_no_audio_features,
        reason='No known track without audio features'
    )
    def test_track_audio_features_not_found_raises(self, app_client):
        with pytest.raises(HTTPError):
            app_client.track_audio_features(track_no_audio_features)

    @pytest.mark.skipif(
        not track_no_audio_features,
        reason='No known track without audio features'
    )
    def test_tracks_audio_features_not_found_is_none(self, app_client):
        features = app_client.tracks_audio_features([track_no_audio_features])
        assert features[0] is None

    def test_track_from_token(self, user_client):
        track = user_client.track(track_id, market='from_token')
        assert track.id == track_id

    def test_tracks_from_token(self, user_client):
        tracks = user_client.tracks(track_ids, market='from_token')
        assert len(tracks) == len(track_ids)
