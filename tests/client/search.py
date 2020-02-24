from requests import HTTPError

from tests._cred import TestCaseWithUserCredentials
from tekore.client.api import SpotifySearch


class TestSpotifySearch(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifySearch(self.user_token)

    def test_search(self):
        self.client.search('sheeran')

    def test_search_below_limit_succeeds(self):
        self.client.search('piano', types=('playlist',), limit=1, offset=1999)

    def test_search_beyond_limit_raises(self):
        with self.assertRaises(HTTPError):
            self.client.search('piano', types=('playlist',), limit=1, offset=2000)
