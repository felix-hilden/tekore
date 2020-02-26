from unittest import TestCase
from unittest.mock import MagicMock

from tekore.client import Spotify
from tests._cred import TestCaseWithCredentials


class TestSpotifyBaseUnits(TestCase):
    def setUp(self):
        self.client = Spotify('token')

    def test_new_token_used_in_context(self):
        with self.client.token_as('new'):
            self.assertEqual(self.client.token, 'new')

    def test_old_token_restored_after_context(self):
        with self.client.token_as('new'):
            pass
        self.assertEqual(self.client.token, 'token')

    def test_next_with_no_next_set_returns_none(self):
        paging = MagicMock()
        paging.next = None

        next_ = self.client.next(paging)
        self.assertIsNone(next_)

    def test_previous_with_no_previous_set_returns_none(self):
        paging = MagicMock()
        paging.previous = None

        previous = self.client.previous(paging)
        self.assertIsNone(previous)


class TestSpotifyMaxLimits(TestCaseWithCredentials):
    def test_turning_on_max_limits_returns_more(self):
        client = Spotify(self.app_token)
        s1, = client.search('piano')
        with client.max_limits(True):
            s2, = client.search('piano')

        self.assertLess(s1.limit, s2.limit)

    def test_turning_off_max_limits_returns_less(self):
        client = Spotify(self.app_token, max_limits_on=True)
        s1, = client.search('piano')
        with client.max_limits(False):
            s2, = client.search('piano')

        self.assertGreater(s1.limit, s2.limit)

    def test_specifying_limit_kwarg_overrides_max_limits(self):
        client = Spotify(self.app_token, max_limits_on=True)
        s, = client.search('piano', limit=1)

        self.assertEqual(s.limit, 1)

    def test_specifying_limit_pos_arg_overrides_max_limits(self):
        client = Spotify(self.app_token, max_limits_on=True)
        s, = client.search('piano', ('track',), None, None, 1)

        self.assertEqual(s.limit, 1)

    def test_specifying_pos_args_until_limit(self):
        client = Spotify(self.app_token, max_limits_on=True)
        s1, = client.search('piano', ('track',), None, None)
        with client.max_limits(False):
            s2, = client.search('piano', ('track',), None, None)

        self.assertGreater(s1.limit, s2.limit)
