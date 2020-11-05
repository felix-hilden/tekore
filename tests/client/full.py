import pytest
from inspect import getmembers, ismethod
from unittest.mock import MagicMock

from tekore import BadRequest, Spotify, Scope
from tekore.model import ModelList
from tekore._client.chunked import chunked, return_none, return_last


@pytest.fixture()
def client():
    """
    Returns a client.

    Args:
    """
    return Spotify('token')


class TestSpotifyUnits:
    def test_new_token_used_in_context(self, client):
        """
        Create a new token.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        with client.token_as('new'):
            assert client.token == 'new'

    def test_old_token_restored_after_context(self, client):
        """
        A context manager hashed.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        with client.token_as('new'):
            pass
        assert client.token == 'token'

    def test_next_with_no_next_set_returns_none(self, client):
        """
        Test for next set of next set of results.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        paging = MagicMock()
        paging.next = None

        next_ = client.next(paging)
        assert next_ is None

    def test_previous_with_no_previous_set_returns_none(self, client):
        """
        Test if a previous test set is_previous.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        paging = MagicMock()
        paging.previous = None

        previous = client.previous(paging)
        assert previous is None

    def test_all_endpoints_have_scope_attributes(self, client):
        """
        Test if all required endpoints are required.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        # Skip non-endpoint functions
        skips = {
            'send',
            'close',
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

    def test_request_with_closed_client_raises(self):
        """
        Test if the request is closed.

        Args:
            self: (todo): write your description
        """
        client = Spotify()
        client.close()
        with pytest.raises(RuntimeError):
            client.track('id')

    @pytest.mark.asyncio
    async def test_request_with_closed_async_client_raises(self):
          """
          Test if the request.

          Args:
              self: (todo): write your description
          """
        client = Spotify(asynchronous=True)
        await client.close()
        with pytest.raises(RuntimeError):
            await client.track('id')


class TestSpotifyMaxLimits:
    def test_turning_on_max_limits_returns_more(self, app_token):
        """
        Test for backends on on_turn limits.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
        """
        client = Spotify(app_token)
        s1, = client.search('piano')
        with client.max_limits(True):
            s2, = client.search('piano')

        assert s1.limit < s2.limit

    def test_turning_off_max_limits_returns_less(self, app_token):
        """
        Test if we have enough to - max limits.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
        """
        client = Spotify(app_token, max_limits_on=True)
        s1, = client.search('piano')
        with client.max_limits(False):
            s2, = client.search('piano')

        assert s1.limit > s2.limit

    def test_specifying_limit_kwarg_overrides_max_limits(self, app_token):
        """
        Test if we have a limit limit limit limit limits.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
        """
        client = Spotify(app_token, max_limits_on=True)
        s, = client.search('piano', limit=1)

        assert s.limit == 1

    def test_specifying_limit_pos_arg_overrides_max_limits(self, app_token):
        """
        Test if limit limit limit limit is set.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
        """
        client = Spotify(app_token, max_limits_on=True)
        s, = client.search('piano', ('track',), None, None, 1)

        assert s.limit == 1

    def test_specifying_pos_args_until_limit(self, app_token):
        """
        Test if the limit of the position of a limit

        Args:
            self: (todo): write your description
            app_token: (str): write your description
        """
        client = Spotify(app_token, max_limits_on=True)
        s1, = client.search('piano', ('track',), None, None)
        with client.max_limits(False):
            s2, = client.search('piano', ('track',), None, None)

        assert s1.limit > s2.limit


@pytest.fixture(scope='class')
def track_ids(data_client):
    """
    Get track ids

    Args:
        data_client: (todo): write your description
    """
    tracks = data_client.playlist_items('37i9dQZF1DX5Ejj0EkURtP')
    return [t.track.id for t in tracks.items]


@pytest.mark.usefixtures('suppress_warnings')
class TestSpotifyChunked:
    def test_too_many_tracks_raises(self, app_client, track_ids):
        """
        Test if a list of tracks have completed.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
            track_ids: (str): write your description
        """
        with pytest.raises(BadRequest):
            app_client.tracks(track_ids)

    @pytest.mark.asyncio
    async def test_async_too_many_tracks_raises(self, app_aclient, track_ids):
          """
          Test if a list tracks.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
              track_ids: (str): write your description
          """
        with pytest.raises(BadRequest):
            await app_aclient.tracks(track_ids)

    def test_too_many_chunked_succeeds(self, app_token, track_ids):
        """
        Test if a list of a list.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
            track_ids: (int): write your description
        """
        client = Spotify(app_token, chunked_on=True)
        tracks = client.tracks(track_ids)
        assert len(track_ids) == len(tracks)

    @pytest.mark.asyncio
    async def test_async_too_many_chunked_succeeds(self, app_token, track_ids):
          """
          Test if a list of a list of tracks were opened.

          Args:
              self: (todo): write your description
              app_token: (str): write your description
              track_ids: (int): write your description
          """
        client = Spotify(app_token, chunked_on=True, asynchronous=True)
        tracks = await client.tracks(track_ids)
        assert len(track_ids) == len(tracks)
        await client.close()

    def test_returns_model_list(self, app_token, track_ids):
        """
        : param app_token : class :. models.

        Args:
            self: (todo): write your description
            app_token: (str): write your description
            track_ids: (str): write your description
        """
        client = Spotify(app_token, chunked_on=True)
        tracks = client.tracks(track_ids)
        assert isinstance(tracks, ModelList)

    def test_chunked_context_enables(self):
        """
        A context for chunked context.

        Args:
            self: (todo): write your description
        """
        client = Spotify()
        with client.chunked(True):
            assert client.chunked_on is True

    def test_chunked_context_disables(self):
        """
        A context manager tomodifies the chunked.

        Args:
            self: (todo): write your description
        """
        client = Spotify(chunked_on=True)
        with client.chunked(False):
            assert client.chunked_on is False


def mock_spotify():
    """
    Return a mock :.

    Args:
    """
    slf = MagicMock()
    slf.chunked_on = True
    slf.is_async = False
    return slf


class TestSpotifyChunkedUnit:
    def test_chunked_return_none(self):
        """
        Decorator that returns a chunked chunked chunked chunked chunked chunked_chunk.

        Args:
            self: (todo): write your description
        """
        func = MagicMock()

        dec = chunked('a', 1, 10, return_none)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r is None

    def test_chunked_return_last(self):
        """
        Return a chunked chunked chunk.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1, 2])

        dec = chunked('a', 1, 10, return_last)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r == 1

    def test_argument_chain_positional(self):
        """
        Returns a list of arguments the chain chain.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, chain='ch', chain_pos=2)(func)
        r = dec(slf, list(range(20)), None)
        func.assert_called_with(slf, list(range(10, 20)), 0)
        assert r == 1

    def test_argument_chain_keyword(self):
        """
        Returns a tuple of the arguments that were passed to the function.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, chain='ch', chain_pos=2)(func)
        r = dec(slf, list(range(20)), ch=None)
        func.assert_called_with(slf, list(range(10, 20)), ch=0)
        assert r == 1

    def test_reverse_when_rev_argument_specified_positional(self):
        """
        Decorator that maps to the reverse of the middleware.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)), 1)
        func.assert_called_with(slf, list(range(10)), 1)
        assert r == 1

    def test_reverse_when_rev_argument_specified_keyword(self):
        """
        Return a tuple of integers ) reverse ) where the caller. ).

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)), rev=1)
        func.assert_called_with(slf, list(range(10)), rev=1)
        assert r == 1

    def test_dont_reverse_when_rev_argument_not_specified(self):
        """
        Decor of reverse reverse reverse reverse reverse of the mock.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked('a', 1, 10, return_last, reverse='rev', reverse_pos=2)(func)
        r = dec(slf, list(range(20)))
        func.assert_called_with(slf, list(range(10, 20)))
        assert r == 1

    def test_chunked_as_kwarg(self):
        """
        Return a chunked chunked chunked chunked chunked.

        Args:
            self: (todo): write your description
        """
        func = MagicMock(side_effect=[0, 1])

        dec = chunked('a', 2, 10, return_last)(func)
        r = dec(mock_spotify(), 0, a=list(range(20)))
        assert r == 1
