from tests._cred import TestCaseWithUserCredentials
from ._resources import user_id


class TestSpotifyUser(TestCaseWithUserCredentials):
    def test_user(self):
        user = self.client.user(user_id)
        self.assertEqual(user.id, user_id)

    def test_current_user(self):
        self.client.current_user()
