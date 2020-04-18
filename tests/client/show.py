from tests._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from ._resources import show_id, show_ids

from requests import HTTPError


class TestSpotifyShowAsApp(TestCaseWithCredentials):
    def test_show_not_found_without_market(self):
        with self.assertRaises(HTTPError):
            self.client.show(show_id)

    def test_show_found_with_market(self):
        show = self.client.show(show_id, market='FI')
        self.assertEqual(show.id, show_id)

    def test_shows(self):
        shows = self.client.shows(show_ids, market='FI')
        self.assertListEqual(show_ids, [s.id for s in shows])

    def test_show_episodes(self):
        episodes = self.client.show_episodes(show_id, market='FI', limit=1)
        self.assertIsNotNone(episodes.items[0])


class TestSpotifyShowAsUser(TestCaseWithUserCredentials):
    def test_show_found_without_market(self):
        show = self.client.show(show_id)
        self.assertEqual(show_id, show.id)
