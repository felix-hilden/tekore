import asyncio
from inspect import getmembers, ismethod
from unittest.mock import MagicMock

import pytest

from tekore import BadRequest, Scope, Spotify, Unauthorised
from tekore._client.chunked import chunked, return_last, return_none


@pytest.fixture
def client():
    return Spotify("token")


async def sleep(k):
    return await asyncio.sleep(k * 0.01)


class TestSpotifyUnits:
    def test_set_token_without_context(self, client):
        client.token = "new"
        assert client.token == "new"

    def test_new_token_used_in_context(self, client):
        with client.token_as("new"):
            assert client.token == "new"

    def test_old_token_restored_after_context(self, client):
        with client.token_as("new"):
            pass
        assert client.token == "token"

    def test_setting_token_in_context_returns_set(self, client):
        with client.token_as("new"):
            client.token = "set"
            assert client.token == "set"

    def test_setting_token_in_context_reset_after_context(self, client):
        with client.token_as("new"):
            client.token = "set"
        assert client.token == "token"

    def test_set_max_limits_without_context(self, client):
        client.max_limits_on = True
        assert client.max_limits_on is True

    def test_new_max_limits_used_in_context(self, client):
        with client.max_limits(on=True):
            assert client.max_limits_on is True

    def test_old_max_limits_restored_after_context(self, client):
        with client.max_limits(on=True):
            pass
        assert client.max_limits_on is False

    def test_setting_max_limits_in_context_returns_set(self, client):
        with client.max_limits(on=True):
            client.max_limits_on = False
            assert client.max_limits_on is False

    def test_setting_max_limits_in_context_reset_after_context(self, client):
        with client.max_limits(on=True):
            client.max_limits_on = True
        assert client.max_limits_on is False

    def test_set_chunked_without_context(self, client):
        client.chunked_on = True
        assert client.chunked_on is True

    def test_new_chunked_used_in_context(self, client):
        with client.chunked(on=True):
            assert client.chunked_on is True

    def test_old_chunked_restored_after_context(self, client):
        with client.chunked(on=True):
            pass
        assert client.chunked_on is False

    def test_setting_chunked_in_context_returns_set(self, client):
        with client.chunked(on=True):
            client.chunked_on = False
            assert client.chunked_on is False

    def test_setting_chunked_in_context_reset_after_context(self, client):
        with client.chunked(on=True):
            client.chunked_on = True
        assert client.chunked_on is False

    @pytest.mark.asyncio
    async def test_token_async_interrupt_preserves_context(self, client):
        async def do_a():
            with client.token_as("a"):
                assert client.token == "a"
                await sleep(1)
                assert client.token == "a"

        async def do_b():
            with client.token_as("b"):
                assert client.token == "b"
                await sleep(1)
                assert client.token == "b"

        await asyncio.gather(do_a(), do_b())

    @pytest.mark.asyncio
    async def test_token_set_visible_in_another_task(self, client):
        async def do_a():
            client.token = "a"

        async def do_b():
            await sleep(1)
            assert client.token == "a"

        await asyncio.gather(do_a(), do_b())

    @pytest.mark.asyncio
    async def test_token_context_unaffected_by_set_in_another_task(self, client):
        async def do_a():
            with client.token_as("a"):
                await sleep(2)
                assert client.token == "a"

        async def do_b():
            await sleep(1)
            client.token = "b"

        await asyncio.gather(do_a(), do_b())

    @pytest.mark.asyncio
    async def test_token_set_without_context_modifies_persistent_value(self, client):
        async def do_a():
            with client.token_as("a"):
                await sleep(2)
            assert client.token == "b"

        async def do_b():
            await sleep(1)
            client.token = "b"

        await asyncio.gather(do_a(), do_b())

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
        # Skip non-endpoint functions
        skips = {
            "send",
            "close",
            "next",
            "previous",
            "all_pages",
            "all_items",
            "chunked",
            "max_limits",
            "token_as",
            "follow_short_link",
        }
        for name, method in getmembers(client, predicate=ismethod):
            if name.startswith("_") or name in skips:
                continue
            assert isinstance(method.scope, Scope)
            assert isinstance(method.required_scope, Scope)
            assert isinstance(method.optional_scope, Scope)
            assert method.scope == method.required_scope + method.optional_scope

    def test_request_with_closed_client_raises(self):
        client = Spotify()
        client.close()
        with pytest.raises(RuntimeError):
            client.track("id")

    @pytest.mark.asyncio
    async def test_request_with_closed_async_client_raises(self):
        client = Spotify(asynchronous=True)
        await client.close()
        with pytest.raises(RuntimeError):
            await client.track("id")

    def test_unauthorised_contains_missing_scopes(self, httpx_mock):
        httpx_mock.add_response(401)
        client = Spotify("token")
        func = client.playback
        with pytest.raises(Unauthorised) as e:
            func()
        assert e.value.required_scope == func.required_scope
        assert e.value.optional_scope == func.optional_scope
        assert e.value.scope == func.scope

    @pytest.mark.asyncio
    async def test_async_unauthorised_contains_missing_scopes(self, httpx_mock):
        httpx_mock.add_response(401)
        client = Spotify("token", asynchronous=True)
        func = client.playback
        with pytest.raises(Unauthorised) as e:
            await func()
        assert e.value.required_scope == func.required_scope
        assert e.value.optional_scope == func.optional_scope
        assert e.value.scope == func.scope


@pytest.mark.api
class TestSpotifyMaxLimits:
    def test_turning_on_max_limits_returns_more(self, app_token):
        client = Spotify(app_token)
        (s1,) = client.search("piano")
        with client.max_limits(on=True):
            (s2,) = client.search("piano")

        assert s1.limit < s2.limit
        client.close()

    def test_turning_off_max_limits_returns_less(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        (s1,) = client.search("piano")
        with client.max_limits(on=False):
            (s2,) = client.search("piano")

        assert s1.limit > s2.limit
        client.close()

    def test_specifying_limit_kwarg_overrides_max_limits(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        (s,) = client.search("piano", limit=1)

        assert s.limit == 1
        client.close()

    def test_specifying_limit_pos_arg_overrides_max_limits(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        (s,) = client.search("piano", ("track",), None, None, 1)

        assert s.limit == 1
        client.close()

    def test_specifying_pos_args_until_limit(self, app_token):
        client = Spotify(app_token, max_limits_on=True)
        (s1,) = client.search("piano", ("track",), None, None)
        with client.max_limits(on=False):
            (s2,) = client.search("piano", ("track",), None, None)

        assert s1.limit > s2.limit
        client.close()


@pytest.fixture(scope="class")
def track_ids(data_client):
    tracks = data_client.playlist_items("37i9dQZF1DX5Ejj0EkURtP")
    return [t.track.id for t in tracks.items]


@pytest.mark.api
@pytest.mark.usefixtures("suppress_warnings")
class TestSpotifyChunked:
    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_too_many_tracks_raises(self, app_client, track_ids):
        with pytest.raises(BadRequest):
            app_client.tracks(track_ids)

    @pytest.mark.xfail(reason="API inconsistencies.")
    @pytest.mark.asyncio
    async def test_async_too_many_tracks_raises(self, app_aclient, track_ids):
        with pytest.raises(BadRequest):
            await app_aclient.tracks(track_ids)

    def test_too_many_chunked_succeeds(self, app_token, track_ids):
        client = Spotify(app_token, chunked_on=True)
        tracks = client.tracks(track_ids)
        assert len(track_ids) == len(tracks)
        client.close()

    @pytest.mark.asyncio
    async def test_async_too_many_chunked_succeeds(self, app_token, track_ids):
        client = Spotify(app_token, chunked_on=True, asynchronous=True)
        tracks = await client.tracks(track_ids)
        assert len(track_ids) == len(tracks)
        await client.close()

    def test_chunked_context_enables(self):
        client = Spotify()
        with client.chunked(on=True):
            assert client.chunked_on is True
        client.close()

    def test_chunked_context_disables(self):
        client = Spotify(chunked_on=True)
        with client.chunked(on=False):
            assert client.chunked_on is False
        client.close()


def mock_spotify():
    slf = MagicMock()
    slf.chunked_on = True
    slf.is_async = False
    return slf


class TestSpotifyChunkedUnit:
    def test_chunked_return_none(self):
        func = MagicMock()

        dec = chunked("a", 1, 10, return_none)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r is None

    def test_chunked_return_last(self):
        func = MagicMock(side_effect=[0, 1, 2])

        dec = chunked("a", 1, 10, return_last)(func)
        r = dec(mock_spotify(), list(range(20)))
        assert r == 1

    def test_chunked_return_last_with_empty_input_returns_none(self):
        func = MagicMock(side_effect=[0, 1, 2])

        dec = chunked("a", 1, 10, return_last)(func)
        r = dec(mock_spotify(), [])
        assert r is None

    def test_argument_chain_positional(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked("a", 1, 10, return_last, chain="ch", chain_pos=2)(func)
        r = dec(slf, list(range(20)), None)
        func.assert_called_with(slf, list(range(10, 20)), 0)
        assert r == 1

    def test_argument_chain_keyword(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked("a", 1, 10, return_last, chain="ch", chain_pos=2)(func)
        r = dec(slf, list(range(20)), ch=None)
        func.assert_called_with(slf, list(range(10, 20)), ch=0)
        assert r == 1

    def test_reverse_when_rev_argument_specified_positional(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked("a", 1, 10, return_last, reverse="rev", reverse_pos=2)(func)
        r = dec(slf, list(range(20)), 1)
        func.assert_called_with(slf, list(range(10)), 1)
        assert r == 1

    def test_reverse_when_rev_argument_specified_keyword(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked("a", 1, 10, return_last, reverse="rev", reverse_pos=2)(func)
        r = dec(slf, list(range(20)), rev=1)
        func.assert_called_with(slf, list(range(10)), rev=1)
        assert r == 1

    def test_dont_reverse_when_rev_argument_not_specified(self):
        func = MagicMock(side_effect=[0, 1])
        slf = mock_spotify()

        dec = chunked("a", 1, 10, return_last, reverse="rev", reverse_pos=2)(func)
        r = dec(slf, list(range(20)))
        func.assert_called_with(slf, list(range(10, 20)))
        assert r == 1

    def test_chunked_as_kwarg(self):
        func = MagicMock(side_effect=[0, 1])

        dec = chunked("a", 2, 10, return_last)(func)
        r = dec(mock_spotify(), 0, a=list(range(20)))
        assert r == 1
