import pytest
from ._resources import (
    track_id,
    track_ids,
    track_relinked,
    track_restricted,
    track_no_audio_features,
    album_id,
)
from tekore import HTTPError


class TestSpotifyTrack:
    def test_track_with_market(self, app_client):
        """
        Test if a track is a tracked.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        track = app_client.track(track_id, market='US')
        assert track.id == track_id
        assert len(track.available_markets) == 0
        assert track.is_playable is not None

    def test_track_no_market(self, app_client):
        """
        : param app_client.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        track = app_client.track(track_id, market=None)
        assert track.id == track_id
        assert len(track.available_markets) > 0
        assert track.is_playable is None

    def test_track_restricted(self, app_client):
        """
        Test if a track track to track.

        Args:
            self: (todo): write your description
            app_client: (str): write your description
        """
        track = app_client.track(track_restricted, market='SE')

        assert track.is_playable is False
        assert track.restrictions.reason == 'market'

    def test_track_relinking(self, app_client):
        """
        Test for track_client.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        track = app_client.track(track_relinked, market='US')

        assert track_relinked != track.id
        assert track_relinked == track.linked_from.id
        assert track.is_playable is True

    def test_tracks_with_market(self, app_client):
        """
        Test if a list of a list of tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.tracks(track_ids, market='US')
        assert len(tracks) == len(track_ids)
        assert all(track.available_markets is None for track in tracks)
        assert all(track.is_playable is not None for track in tracks)

    def test_tracks_no_market(self, app_client):
        """
        Test if the specified tracks is the given tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.tracks(track_ids, market=None)
        assert len(tracks) == len(track_ids)
        assert all(len(track.available_markets) > 0 for track in tracks)
        assert all(track.is_playable is None for track in tracks)

    def test_simple_tracks_with_market(self, app_client):
        """
        Test for all tracks in a given.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album(album_id, market='US').tracks.items
        assert all(track.available_markets is None for track in tracks)
        assert all(track.is_playable is not None for track in tracks)

    def test_simple_tracks_no_market(self, app_client):
        """
        Test for a simple tracks has a simple simple tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album(album_id, market=None).tracks.items
        assert all(len(track.available_markets) > 0 for track in tracks)
        assert all(track.is_playable is None for track in tracks)

    def test_track_audio_analysis(self, app_client):
        """
        Test if the analysis analysis analysis.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        app_client.track_audio_analysis(track_id)

    def test_track_audio_features(self, app_client):
        """
        Test if track track track track track.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        features = app_client.track_audio_features(track_id)
        assert features.id == track_id

    def test_tracks_audio_features(self, app_client):
        """
        Test for tracks tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        features = app_client.tracks_audio_features(track_ids)
        assert [f.id for f in features] == track_ids

    @pytest.mark.skipif(
        not track_no_audio_features,
        reason='No known track without audio features'
    )
    def test_track_audio_features_not_found_raises(self, app_client):
        """
        Test if audio audio audio audio audio audio audio track.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(HTTPError):
            app_client.track_audio_features(track_no_audio_features)

    @pytest.mark.skipif(
        not track_no_audio_features,
        reason='No known track without audio features'
    )
    def test_tracks_audio_features_not_found_is_none(self, app_client):
        """
        Test if audio audio audio audio audio audio audio audio audio audio audio.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        features = app_client.tracks_audio_features([track_no_audio_features])
        assert features[0] is None

    def test_track_from_token(self, user_client):
        """
        Test if a track from a track.

        Args:
            self: (todo): write your description
            user_client: (str): write your description
        """
        track = user_client.track(track_id, market='from_token')
        assert track.id == track_id

    def test_tracks_from_token(self, user_client):
        """
        Get tracks from a list of tracks.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        tracks = user_client.tracks(track_ids, market='from_token')
        assert len(tracks) == len(track_ids)
