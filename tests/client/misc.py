from ._cred import TestCaseWithUserCredentials
from ._resources import user_id

from spotipy.client import Spotify


class TestSpotifyFollow(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

    def test_search(self):
        self.client.search('sheeran')

    def test_user(self):
        user = self.client.user(user_id)
        self.assertEqual(user.id, user_id)

    def test_current_user(self):
        self.client.current_user()

    def test_cu_top_artists(self):
        self.client.current_user_top_artists()

    def test_cu_top_tracks(self):
        self.client.current_user_top_tracks()
