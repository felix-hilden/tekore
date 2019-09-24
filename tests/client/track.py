from ._cred import TestCaseWithCredentials
from spotipy.client import SpotifyTrack


class TestSpotifyTrack(TestCaseWithCredentials):
    track_id = '1OtGh4nRaCYGisPJwubjvz'
    track_ids = [track_id, '2GV41X8idjOWKpKwUKIDJ6']

    def setUp(self):
        self.client = SpotifyTrack(self.app_token)

    def test_track_with_market(self):
        track = self.client.track(self.track_id, market='US')
        self.assertEqual(track.id, self.track_id)

    def test_track_no_market(self):
        track = self.client.track(self.track_id, market=None)
        self.assertEqual(track.id, self.track_id)

    def test_tracks_with_market(self):
        tracks = self.client.tracks(self.track_ids, market='US')
        self.assertEqual(len(tracks), 2)

    def test_tracks_no_market(self):
        tracks = self.client.tracks(self.track_ids, market=None)
        self.assertEqual(len(tracks), 2)

    def test_track_audio_analysis(self):
        self.client.track_audio_analysis(self.track_id)

    def test_track_audio_features(self):
        features = self.client.track_audio_features(self.track_id)
        self.assertEqual(features.id, self.track_id)

    def test_tracks_audio_features(self):
        features = self.client.tracks_audio_features(self.track_ids)
        self.assertListEqual([f.id for f in features], self.track_ids)
