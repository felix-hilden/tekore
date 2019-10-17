from ._cred import TestCaseWithUserCredentials
from ._resources import user_id

from spotipy.client import Spotify


class TestSpotifyFollow(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

    def test_search(self):
        self.client.search('sheeran')

    def test_search_paging_next(self):
        cat, = self.client.search('sheeran', limit=1)
        cat_next = self.client.next(cat)
        self.assertGreater(cat_next.total, 0)

    def test_search_paging_previous(self):
        cat, = self.client.search('sheeran', limit=1)
        cat_next = self.client.next(cat)
        cat_prev = self.client.previous(cat_next)
        self.assertEqual(cat.items[0].id, cat_prev.items[0].id)

    def test_user(self):
        user = self.client.user(user_id)
        self.assertEqual(user.id, user_id)

    def test_current_user(self):
        self.client.current_user()

    def test_cu_top_artists(self):
        self.client.current_user_top_artists()

    def test_cu_top_tracks(self):
        self.client.current_user_top_tracks()
