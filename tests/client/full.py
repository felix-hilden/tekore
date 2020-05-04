from asyncio import run
from unittest import TestCase
from unittest.mock import MagicMock

from tekore import BadRequest, Spotify
from tekore._client.chunked import chunked, return_none, return_last
from tests._cred import TestCaseWithCredentials, TestCaseWithUserCredentials
from tests._util import handle_warnings


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


class TestSpotifyChunked(TestCaseWithUserCredentials):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        tracks = cls.client.playlist_tracks('37i9dQZF1DX5Ejj0EkURtP')
        cls.track_ids = [t.track.id for t in tracks.items]

        cls.handle = handle_warnings()
        cls.handle.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.handle.__exit__(None, None, None)

    def test_too_many_tracks_raises(self):
        client = Spotify(self.app_token)

        with self.assertRaises(BadRequest):
            client.tracks(self.track_ids)

    def test_async_too_many_tracks_raises(self):
        client = Spotify(self.app_token, asynchronous=True)

        with self.assertRaises(BadRequest):
            run(client.tracks(self.track_ids))

    def test_too_many_tracks_chunked_succeeds(self):
        client = Spotify(self.app_token, chunked_on=True)
        tracks = client.tracks(self.track_ids)
        self.assertEqual(len(self.track_ids), len(tracks))

    def test_async_too_many_tracks_chunked_succeeds(self):
        client = Spotify(self.app_token, chunked_on=True, asynchronous=True)
        tracks = run(client.tracks(self.track_ids))
        self.assertEqual(len(self.track_ids), len(tracks))

    def test_chunked_context_enables(self):
        client = Spotify(self.app_token)
        with client.chunked(True):
            self.assertTrue(client.chunked_on)

    def test_chunked_context_disables(self):
        client = Spotify(self.app_token, chunked_on=True)
        with client.chunked(False):
            self.assertFalse(client.chunked_on)


def mock_spotify():
    slf = MagicMock()
    slf.chunked_on = True
    slf.is_async = False
    return slf


class TestSpotifyChunkedUnit(TestCase):
    def test_chunked_return_none(self):
        func = MagicMock()

        dec = chunked('a', 1, 10, return_none)(func)
        r = dec(mock_spotify(), list(range(20)))
        self.assertIsNone(r)

    def test_chunked_return_last(self):
        func = MagicMock(side_effect=[0, 1, 2])

        dec = chunked('a', 1, 10, return_last)(func)
        r = dec(mock_spotify(), list(range(20)))
        self.assertEqual(r, 1)

    def test_argument_chain(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, chain='ch', chain_pos=2)(func)
        r = dec(slf, list(range(20)), ch=None)
        func.assert_called_with(slf, list(range(10, 20)), ch=0)
        self.assertEqual(r, 1)

    def test_reverse_when_rev_argument_specified(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)), rev=1)
        func.assert_called_with(slf, list(range(10)), rev=1)
        self.assertEqual(r, 1)

    def test_dont_reverse_when_rev_argument_not_specified(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)))
        func.assert_called_with(slf, list(range(10, 20)))
        self.assertEqual(r, 1)

    def test_chunked_as_kwarg(self):
        func = MagicMock(side_effect=[0, 1])

        dec = chunked('a', 2, 10, return_last)(func)
        r = dec(mock_spotify(), 0, a=list(range(20)))
        self.assertEqual(r, 1)
