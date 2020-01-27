from tests._cred import TestCaseWithUserCredentials
from ._resources import user_id

from tekore.client.api import SpotifyUser


class TestSpotifyUser(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyUser(self.user_token)

    def test_user(self):
        user = self.client.user(user_id)
        self.assertEqual(user.id, user_id)

    def test_current_user(self):
        self.client.current_user()
