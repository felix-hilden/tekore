import pytest
from inspect import getmembers, ismethod
from unittest.mock import MagicMock

from tekore import BadRequest, Spotify
from tekore._auth import Scope
from tekore._client.chunked import chunked, return_none, return_last


@pytest.fixture()
def client():
    return Spotify('token')


class TestSpotifyUnits:
    def test_new_token_used_in_context(self, client):
        with client.token_as('new'):
            assert client.token == 'new'

    def test_old_token_restored_after_context(self, client):
        with client.token_as('new'):
            pass
        assert client.token == 'token'

    def test_next_with_no_next_set_returns_none(self, client):
        paging = MagicMock()
        paging.next = None

        next_ = client.next(paging)
        assert next_ is None

    def test_previous_with_no_previous_set_returns_none(self, client):
        paging = MagicMock()
        paging.previous = None

        previous = client.previous(paging)
        assert previous is None

    def test_all_endpoints_have_scope_attributes(self, client):
        # Skip paging calls and options
        skips = {
            'next',
            'previous',
            'all_pages',
            'all_items',
            'chunked',
            'max_limits',
            'token_as',
        }
        for name, method in getmembers(client, predicate=ismethod):
            if name.startswith('_') or name in skips:
                continue
            assert isinstance(method.scope, Scope)
            assert isinstance(method.required_scope, Scope)
            assert isinstance(method.optional_scope, Scope)
            assert method.scope == method.required_scope + method.optional_scope


class TestSpotifyMaxLimits:
    def test_turning_on_max_limits_returns_more(self, app_token):
        client = Spotify(app_token)
        s1, = client.search('piano')
        with client.max_limits(True):
            s2, = client.search('piano')

        assert s1.limit < s2.limit

    def test_turning_off_max_limits_returns_less(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        s1, = client.search('piano')
        with client.max_limits(False):
            s2, = client.search('piano')

        assert s1.limit > s2.limit

    def test_specifying_limit_kwarg_overrides_max_limits(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        s, = client.search('piano', limit=1)

        assert s.limit == 1

    def test_specifying_limit_pos_arg_overrides_max_limits(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        s, = client.search('piano', ('track',), None, None, 1)

        assert s.limit == 1

    def test_specifying_pos_args_until_limit(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        s1, = client.search('piano', ('track',), None, None)
        with client.max_limits(False):
            s2, = client.search('piano', ('track',), None, None)

        assert s1.limit > s2.limit


@pytest.fixture(scope='class')
def track_ids(data_client):
    tracks = data_client.playlist_items('37i9dQZF1DX5Ejj0EkURtP')
    return [t.track.id for t in tracks.items]


@pytest.mark.usefixtures('suppress_warnings')
class TestSpotifyChunked:
    def test_too_many_tracks_raises(self, app_client, track_ids):
        with pytest.raises(BadRequest):
            app_client.tracks(track_ids)

    @pytest.mark.asyncio
    async def test_async_too_many_tracks_raises(self, app_aclient, track_ids):
        with pytest.raises(BadRequest):
            await app_aclient.tracks(track_ids)

    def test_too_many_chunked_succeeds(self, app_token, track_ids):
        client = Spotify(app_token, chunked_on=True)
        tracks = client.tracks(track_ids)
        assert len(track_ids) == len(tracks)

    @pytest.mark.asyncio
    async def test_async_too_many_chunked_succeeds(self, app_token, track_ids):
        client = Spotify(app_token, chunked_on=True, asynchronous=True)
        tracks = await client.tracks(track_ids)
        assert len(track_ids) == len(tracks)

    def test_chunked_context_enables(self):
        client = Spotify()
        with client.chunked(True):
            assert client.chunked_on is True

    def test_chunked_context_disables(self):
        client = Spotify(chunked_on=True)
        with client.chunked(False):
            assert client.chunked_on is False


def mock_spotify():
    slf = MagicMock()
    slf.chunked_on = True
    slf.is_async = False
    return slf


class TestSpotifyChunkedUnit:
    def test_chunked_return_none(self):
        func = MagicMock()

        dec = chunked('a', 1, 10, return_none)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r is None

    def test_chunked_return_last(self):
        func = MagicMock(side_effect=[0, 1, 2])

        dec = chunked('a', 1, 10, return_last)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r == 1

    def test_argument_chain(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, chain='ch', chain_pos=2)(func)
        r = dec(slf, list(range(20)), ch=None)
        func.assert_called_with(slf, list(range(10, 20)), ch=0)
        assert r == 1

    def test_reverse_when_rev_argument_specified(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)), rev=1)
        func.assert_called_with(slf, list(range(10)), rev=1)
        assert r == 1

    def test_dont_reverse_when_rev_argument_not_specified(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)))
        func.assert_called_with(slf, list(range(10, 20)))
        assert r == 1

    def test_chunked_as_kwarg(self):
        func = MagicMock(side_effect=[0, 1])

        dec = chunked('a', 2, 10, return_last)(func)
        r = dec(mock_spotify(), 0, a=list(range(20)))
        assert r == 1
