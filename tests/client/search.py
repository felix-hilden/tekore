from ._cred import TestCaseWithUserCredentials
from spotipy.client.api import SpotifySearch


class TestSpotifySearch(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifySearch(self.user_token)

    def test_search(self):
        self.client.search('sheeran')
