from collections.abc import Callable
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

import pytest

from tekore import CachingSender, Request, Response
from tests._util import AsyncMock


def mock_sender(*responses, is_async: bool = False):
    sender = MagicMock()
    sender.is_async = is_async
    if is_async:
        sender.send = AsyncMock(side_effect=responses)
    else:
        sender.send.side_effect = responses
    return sender


def request(url, params, headers) -> Request:
    return Request(method="GET", url=url, params=params, headers=headers)


def response(code, url, params, cc=None, etag=None, vary=None) -> Response:
    r = Response(
        status_code=code,
        url=url + ("&" + urlencode(params) if params else ""),
        headers={},
        content=None,
    )
    if isinstance(cc, int):
        cc = f"public, max-age={cc}"
    h = {"Cache-Control": cc, "ETag": etag, "Vary": vary}
    r.headers = {k: v for k, v in h.items() if v is not None}
    return r


def pair(code, url, params=None, cc=None, etag=None, vary_h=None) -> tuple:
    req = request(url, params or {}, vary_h or {})
    vary = ", ".join(list(vary_h)) if vary_h is not None else None
    res = response(code, url, params or {}, cc, etag, vary)
    return req, res


def multiple(func: Callable, n: int, *args, **kwargs):
    return [func(*args, **kwargs) for _ in range(n)]


module = "tekore._sender.extending"


@pytest.fixture
def sender():
    return CachingSender()


def assert_two_sent(sender, r, p1, p2):
    sender.sender = mock_sender(p1, p2)
    sender.send(r)
    assert sender.send(r) is p2


class TestCachingSender:
    def test_repr(self):
        s = CachingSender()
        assert repr(s).startswith("CachingSender(")

    def test_other_methods_than_get_not_cached(self, sender):
        methods = ("PUT", "POST", "DELETE")

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, "", {}) for _ in requests]
            sender.sender = mock_sender(*responses)
            sent = [sender.send(r) for r in requests]
            assert sent[0] is not sent[1]

    @pytest.mark.asyncio
    async def test_async_other_methods_not_cached(self, sender):
        methods = ("PUT", "POST", "DELETE")

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, "", {}) for _ in requests]
            sender.sender = mock_sender(*responses, is_async=True)
            sent = [await sender.send(r) for r in requests]
            assert sent[0] is not sent[1]

    def test_params_affect_cache_url(self, sender):
        r1, p1 = pair(200, "url", cc=10)
        r2, p2 = pair(200, "url", {"p": 1}, cc=10)

        sender.sender = mock_sender(p1, p2)
        sender.send(r1)
        sender.send(r2)
        assert sender.send(r1) is p1
        assert sender.send(r2) is p2

    def test_vary_affects_caching(self, sender):
        r1, p1 = pair(200, "url", cc=10, vary_h={"h": "a"})
        r2, p2 = pair(200, "url", cc=10, vary_h={"h": "b"})

        sender.sender = mock_sender(p1, p2)
        sender.send(r1)
        sender.send(r2)
        assert sender.send(r1) is p1
        assert sender.send(r2) is p2

    def test_error_not_cached(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 400, "url", {}, cc=10)
        assert_two_sent(sender, r, p1, p2)

    def test_vary_star_not_cached(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, cc=10, vary="*")
        assert_two_sent(sender, r, p1, p2)

    def test_cc_private_not_cached(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, cc="private, max-age=0")
        assert_two_sent(sender, r, p1, p2)

    def test_no_cc_and_no_etag_not_cached(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {})
        assert_two_sent(sender, r, p1, p2)

    def test_no_cc_and_has_etag_not_cached(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, etag="a")
        assert_two_sent(sender, r, p1, p2)

    def test_private_cc_and_has_etag_not_cached(self, sender):
        r = request("url", {}, {})
        cc = "private, max-age=0"
        p1, p2 = multiple(response, 2, 200, "url", {}, cc=cc, etag="a")
        assert_two_sent(sender, r, p1, p2)

    def test_has_cc_and_no_etag_is_cached(self, sender):
        r = request("url", {}, {})
        p = response(200, "url", {}, cc=10)

        sender.sender = mock_sender(p)
        sender.send(r)
        assert sender.send(r) is p

    @pytest.mark.asyncio
    async def test_async_has_cc_and_no_etag_is_cached(self, sender):
        r = request("url", {}, {})
        p = response(200, "url", {}, cc=10)

        sender.sender = mock_sender(p, is_async=True)
        await sender.send(r)
        assert await sender.send(r) is p

    def test_cc_only_new_returned_when_stale(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + ".time.time", time):
            sender.send(r)
            assert sender.send(r) is p2

    def test_cc_only_stale_replaced_with_new(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15, 20])
        with patch(module + ".time.time", time):
            sender.send(r)
            sender.send(r)
            assert sender.send(r) is p2

    def test_etag_only_cached_returned_on_304(self, sender):
        r = request("url", {}, {})
        p1 = response(200, "url", {}, cc=0, etag="a")
        p2 = response(304, "url", {})

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + ".time.time", time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p1
            assert "ETag" in r.headers

    def test_etag_only_fresh_returned_on_success(self, sender):
        r = request("url", {}, {})
        p1 = response(200, "url", {}, cc=0, etag="a")
        p2 = response(200, "url", {}, cc=0, etag="b")

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + ".time.time", time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p2
            assert "ETag" in r.headers

    @pytest.mark.asyncio
    async def test_async_etag_only_fresh_returned_on_success(self, sender):
        r = request("url", {}, {})
        p1 = response(200, "url", {}, cc=0, etag="a")
        p2 = response(200, "url", {}, cc=0, etag="b")

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + ".time.time", time):
            sender.sender = mock_sender(p1, p2, is_async=True)
            await sender.send(r)
            assert await sender.send(r) is p2
            assert "ETag" in r.headers

    def test_etag_only_stale_replaced_with_new(self, sender):
        r = request("url", {}, {})
        p1 = response(200, "url", {}, cc=0, etag="a")
        p2 = response(200, "url", {}, cc=0, etag="b")
        p3 = response(304, "url", {}, cc=0, etag="b")

        time = MagicMock(side_effect=[0, 15, 15, 30, 30])
        with patch(module + ".time.time", time):
            sender.sender = mock_sender(p1, p2, p3)
            sender.send(r)
            sender.send(r)
            assert sender.send(r) is p2

    def test_fresh_cc_precedes_etag(self, sender):
        r = request("url", {}, {})
        p1 = response(200, "url", {}, cc=10, etag="a")
        p2 = response(304, "url", {})

        time = MagicMock(side_effect=[0, 15])
        with patch(module + ".time.time", time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p1

    def test_clear(self, sender):
        r = request("url", {}, {})
        p1, p2 = multiple(response, 2, 200, "url", {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        sender.send(r)
        sender.clear()
        assert sender.send(r) is p2

    def test_exceeding_max_size_drops_first_item(self):
        r1, p1 = pair(200, "url1", cc=3600)
        r2, p2 = pair(200, "url2", cc=3600)
        r3, p3 = pair(200, "url3", cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        with pytest.raises(StopIteration):
            sender.send(r1)

        assert sender.send(r2) is p2

    def test_exceeding_max_size_drops_lru_item(self):
        r1, p1 = pair(200, "url1", cc=3600)
        r2, p2 = pair(200, "url2", cc=3600)
        r3, p3 = pair(200, "url3", cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r1)
        sender.send(r3)

        with pytest.raises(StopIteration):
            sender.send(r2)

        assert sender.send(r1) is p1

    def test_cache_size_not_affected_by_stale_other_items(self):
        r1, p1 = pair(200, "url1", cc=3600)
        r2, p2 = pair(200, "url2", cc=-5)
        r3, p3 = pair(200, "url3", cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        assert sender.send(r1) is p1
        with pytest.raises(StopIteration):
            sender.send(r2)

    def test_cache_size_not_affected_by_stale_same_items(self):
        r1, p1 = pair(200, "url1", cc=3600)
        r2, p2 = pair(200, "url2", cc=-5)
        r3, p3 = pair(200, "url2", cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        assert sender.send(r1) is p1
        assert sender.send(r2) is p3
