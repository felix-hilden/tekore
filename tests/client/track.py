from ._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import track_id, track_ids

from spotipy.client import SpotifyTrack


class TestSpotifyTrack(TestCaseWithCredentials):
    def setUp(self):
        self.client = SpotifyTrack(self.app_token)

    def test_track_with_market(self):
        track = self.client.track(track_id, market='US')
        self.assertEqual(track.id, track_id)

    def test_track_no_market(self):
        track = self.client.track(track_id, market=None)
        self.assertEqual(track.id, track_id)

    def test_track_unplayable(self):
        unplayable = '6F6CuSuM8EcD4UD0N3nuxN'
        track = self.client.track(unplayable, market='SE')
        self.assertEqual(track.id, unplayable)

    def test_tracks_with_market(self):
        tracks = self.client.tracks(track_ids, market='US')
        self.assertEqual(len(tracks), len(track_ids))

    def test_tracks_no_market(self):
        tracks = self.client.tracks(track_ids, market=None)
        self.assertEqual(len(tracks), len(track_ids))

    def test_track_audio_analysis(self):
        self.client.track_audio_analysis(track_id)

    def test_track_audio_features(self):
        features = self.client.track_audio_features(track_id)
        self.assertEqual(features.id, track_id)

    def test_tracks_audio_features(self):
        features = self.client.tracks_audio_features(track_ids)
        self.assertListEqual([f.id for f in features], track_ids)


class TestSpotifyTrackAsUser(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyTrack(self.user_token)

    def test_track_from_token(self):
        track = self.client.track(track_id, market='from_token')
        self.assertEqual(track.id, track_id)

    def test_tracks_from_token(self):
        tracks = self.client.tracks(track_ids, market='from_token')
        self.assertEqual(len(tracks), len(track_ids))
