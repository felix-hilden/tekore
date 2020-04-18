from tests._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import episode_id, episode_ids

from requests import HTTPError


class TestSpotifyEpisodeAsApp(TestCaseWithCredentials):
    def test_episode_not_found_without_market(self):
        with self.assertRaises(HTTPError):
            self.client.episode(episode_id)

    def test_episode_found_with_market(self):
        episode = self.client.episode(episode_id, market='FI')
        self.assertEqual(episode.id, episode_id)

    def test_resume_point_is_none(self):
        episode = self.client.episode(episode_id, market='FI')
        self.assertIsNone(episode.resume_point)

    def test_episodes(self):
        episodes = self.client.episodes(episode_ids, market='FI')
        self.assertListEqual(episode_ids, [e.id for e in episodes])


class TestSpotifyEpisodeAsUser(TestCaseWithUserCredentials):
    def test_found_without_market(self):
        episode = self.client.episode(episode_id)
        self.assertEqual(episode.id, episode_id)

    def test_resume_point_exists(self):
        episode = self.client.episode(episode_id)
        self.assertIsNotNone(episode.resume_point)
