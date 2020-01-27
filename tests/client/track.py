from tests._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import (
    track_id,
    track_ids,
    track_relinked,
    track_restricted,
)

from tekore.client.api import SpotifyTrack


class TestSpotifyTrack(TestCaseWithCredentials):
    def setUp(self):
        self.client = SpotifyTrack(self.app_token)

    def test_track_with_market(self):
        track = self.client.track(track_id, market='US')
        self.assertEqual(track.id, track_id)

    def test_track_with_market_available_markets_not_in_response(self):
        track = self.client.track(track_id, market='US')
        self.assertIsNone(track.available_markets)

    def test_track_no_market(self):
        track = self.client.track(track_id, market=None)
        self.assertEqual(track.id, track_id)

    def test_track_no_market_is_playable_not_in_response(self):
        track = self.client.track(track_id, market=None)
        self.assertIsNone(track.is_playable)

    def test_track_restricted(self):
        track = self.client.track(track_restricted, market='SE')

        with self.subTest('Playable'):
            self.assertFalse(track.is_playable)
        with self.subTest('Restrictions'):
            self.assertEqual(track.restrictions.reason, 'market')

    def test_track_relinking(self):
        track = self.client.track(track_relinked, market='US')

        with self.subTest('ID not equal'):
            self.assertNotEqual(track_relinked, track.id)
        with self.subTest('ID equal to relinked'):
            self.assertEqual(track_relinked, track.linked_from.id)
        with self.subTest('Playable'):
            self.assertTrue(track.is_playable)

    def test_track_doesnt_have_episode_or_track(self):
        track = self.client.track(track_id)
        self.assertTrue(all(i is None for i in (track.episode, track.track)))

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

    # No track without audio features
    # def test_track_audio_features_not_found_raises(self):
    #     with self.assertRaises(HTTPError):
    #         self.client.track_audio_features(track_no_audio_features)

    def test_tracks_audio_features(self):
        features = self.client.tracks_audio_features(track_ids)
        self.assertListEqual([f.id for f in features], track_ids)

    # def test_tracks_audio_features_not_found_is_none(self):
    #     features = self.client.tracks_audio_features([track_no_audio_features])
    #     self.assertIsNone(features[0])


class TestSpotifyTrackAsUser(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyTrack(self.user_token)

    def test_track_from_token(self):
        track = self.client.track(track_id, market='from_token')
        self.assertEqual(track.id, track_id)

    def test_tracks_from_token(self):
        tracks = self.client.tracks(track_ids, market='from_token')
        self.assertEqual(len(tracks), len(track_ids))
