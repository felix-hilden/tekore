import pytest
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

from tekore import CachingSender, Request, Response
from tests._util import AsyncMock


def mock_sender(*responses, is_async: bool = False):
    """
    Perform an http sender.

    Args:
        responses: (todo): write your description
        is_async: (bool): write your description
    """
    sender = MagicMock()
    sender.is_async = is_async
    if is_async:
        sender.send = AsyncMock(side_effect=responses)
    else:
        sender.send.side_effect = responses
    return sender


def request(url, params, headers) -> Request:
    """
    Make a request.

    Args:
        url: (str): write your description
        params: (dict): write your description
        headers: (dict): write your description
    """
    return Request(
        method='GET',
        url=url,
        params=params,
        headers=headers,
    )


def response(code, url, params, cc=None, etag=None, vary=None) -> Response:
    """
    Make a response.

    Args:
        code: (str): write your description
        url: (str): write your description
        params: (dict): write your description
        cc: (todo): write your description
        etag: (str): write your description
        vary: (str): write your description
    """
    r = Response(
        status_code=code,
        url=url + ('&' + urlencode(params) if params else ''),
        headers={},
        content=None
    )
    if isinstance(cc, int):
        cc = f'public, max-age={cc}'
    h = {
        'Cache-Control': cc,
        'ETag': etag,
        'Vary': vary
    }
    r.headers = {k: v for k, v in h.items() if v is not None}
    return r


def pair(code, url, params=None, cc=None, etag=None, vary_h=None) -> tuple:
    """
    Perform a pair of code pair.

    Args:
        code: (str): write your description
        url: (str): write your description
        params: (dict): write your description
        cc: (int): write your description
        etag: (str): write your description
        vary_h: (int): write your description
    """
    req = request(url, params or {}, vary_h or {})
    if vary_h is not None:
        vary = ', '.join([k for k in vary_h])
    else:
        vary = None
    res = response(code, url, params or {}, cc, etag, vary)
    return req, res


def multiple(func: callable, n: int, *args, **kwargs):
    """
    Return a function that takes a list of n times.

    Args:
        func: (todo): write your description
        n: (array): write your description
    """
    return [func(*args, **kwargs) for _ in range(n)]


module = 'tekore._sender.extending'


@pytest.fixture()
def sender():
    """
    Return a new sender

    Args:
    """
    return CachingSender()


def assert_two_sent(sender, r, p1, p2):
    """
    Asserts the two p1 and p2

    Args:
        sender: (todo): write your description
        r: (todo): write your description
        p1: (todo): write your description
        p2: (todo): write your description
    """
    sender.sender = mock_sender(p1, p2)
    sender.send(r)
    assert sender.send(r) is p2


class TestCachingSender:
    def test_repr(self):
        """
        Test if the description of a test.

        Args:
            self: (todo): write your description
        """
        s = CachingSender()
        assert repr(s).startswith('CachingSender(')

    def test_other_methods_than_GET_not_cached(self, sender):
        """
        Test if the method cached method of the http : param sender : : return :

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        methods = ('PUT', 'POST', 'DELETE')

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, '', {}) for _ in requests]
            sender.sender = mock_sender(*responses)
            sent = [sender.send(r) for r in requests]
            assert sent[0] is not sent[1]

    @pytest.mark.asyncio
    async def test_async_other_methods_not_cached(self, sender):
          """
          Test if the method.

          Args:
              self: (todo): write your description
              sender: (todo): write your description
          """
        methods = ('PUT', 'POST', 'DELETE')

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, '', {}) for _ in requests]
            sender.sender = mock_sender(*responses, is_async=True)
            sent = [await sender.send(r) for r in requests]
            assert sent[0] is not sent[1]

    def test_params_affect_cache_url(self, sender):
        """
        Returns the cache url is cached.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r1, p1 = pair(200, 'url', cc=10)
        r2, p2 = pair(200, 'url', {'p': 1}, cc=10)

        sender.sender = mock_sender(p1, p2)
        sender.send(r1)
        sender.send(r2)
        assert sender.send(r1) is p1
        assert sender.send(r2) is p2

    def test_vary_affects_caching(self, sender):
        """
        Test if affects affects between two drive.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r1, p1 = pair(200, 'url', cc=10, vary_h={'h': 'a'})
        r2, p2 = pair(200, 'url', cc=10, vary_h={'h': 'b'})

        sender.sender = mock_sender(p1, p2)
        sender.send(r1)
        sender.send(r2)
        assert sender.send(r1) is p1
        assert sender.send(r2) is p2

    def test_error_not_cached(self, sender):
        """
        Test if the error occurs.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 400, 'url', {}, cc=10)
        assert_two_sent(sender, r, p1, p2)

    def test_vary_star_not_cached(self, sender):
        """
        Determine not_vary.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10, vary='*')
        assert_two_sent(sender, r, p1, p2)

    def test_cc_private_not_cached(self, sender):
        """
        This method : py : py : attr : py : meth :. service : param sender : meth : : return :

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc='private, max-age=0')
        assert_two_sent(sender, r, p1, p2)

    def test_no_cc_and_no_etag_not_cached(self, sender):
        """
        Test if you want_no test.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {})
        assert_two_sent(sender, r, p1, p2)

    def test_no_cc_and_has_etag_not_cached(self, sender):
        """
        Determine the cross - validation.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, etag='a')
        assert_two_sent(sender, r, p1, p2)

    def test_private_cc_and_has_etag_not_cached(self, sender):
        """
        This is a private method is sent to the cross - validation.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        cc = 'private, max-age=0'
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=cc, etag='a')
        assert_two_sent(sender, r, p1, p2)

    def test_has_cc_and_no_etag_is_cached(self, sender):
        """
        Returns true if speaker has_etag_no_no_no_no_no_no is enabled.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p = response(200, 'url', {}, cc=10)

        sender.sender = mock_sender(p)
        sender.send(r)
        assert sender.send(r) is p

    @pytest.mark.asyncio
    async def test_async_has_cc_and_no_etag_is_cached(self, sender):
          """
          Sends and sends and sends a play and send it.

          Args:
              self: (todo): write your description
              sender: (todo): write your description
          """
        r = request('url', {}, {})
        p = response(200, 'url', {}, cc=10)

        sender.sender = mock_sender(p, is_async=True)
        await sender.send(r)
        assert await sender.send(r) is p

    def test_cc_only_new_returned_when_stale(self, sender):
        """
        Test whether a new tests.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + '.time.time', time):
            sender.send(r)
            assert sender.send(r) is p2

    def test_cc_only_stale_replaced_with_new(self, sender):
        """
        Test for a mock side side side of a mock.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15, 20])
        with patch(module + '.time.time', time):
            sender.send(r)
            sender.send(r)
            assert sender.send(r) is p2

    def test_etag_only_cached_returned_on_304(self, sender):
        """
        Test if a cached cached cached test.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(304, 'url', {})

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + '.time.time', time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p1
            assert 'ETag' in r.headers

    def test_etag_only_fresh_returned_on_success(self, sender):
        """
        Test if a response to see if the request.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + '.time.time', time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p2
            assert 'ETag' in r.headers

    @pytest.mark.asyncio
    async def test_async_etag_only_fresh_returned_on_success(self, sender):
          """
          Asynchronously send an etag.

          Args:
              self: (todo): write your description
              sender: (todo): write your description
          """
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15])
        with patch(module + '.time.time', time):
            sender.sender = mock_sender(p1, p2, is_async=True)
            await sender.send(r)
            assert await sender.send(r) is p2
            assert 'ETag' in r.headers

    def test_etag_only_stale_replaced_with_new(self, sender):
        """
        Sends a new etag.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')
        p3 = response(304, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15, 30, 30])
        with patch(module + '.time.time', time):
            sender.sender = mock_sender(p1, p2, p3)
            sender.send(r)
            sender.send(r)
            assert sender.send(r) is p2

    def test_fresh_cc_precedes_etag(self, sender):
        """
        Sends precedes.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=10, etag='a')
        p2 = response(304, 'url', {})

        time = MagicMock(side_effect=[0, 15])
        with patch(module + '.time.time', time):
            sender.sender = mock_sender(p1, p2)
            sender.send(r)
            assert sender.send(r) is p1

    def test_clear(self, sender):
        """
        Clears the sender.

        Args:
            self: (todo): write your description
            sender: (todo): write your description
        """
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        sender.sender = mock_sender(p1, p2)
        sender.send(r)
        sender.clear()
        assert sender.send(r) is p2

    def test_exceeding_max_size_drops_first_item(self):
        """
        Test if the maximum number of the maximum number of maximum.

        Args:
            self: (todo): write your description
        """
        r1, p1 = pair(200, 'url1', cc=3600)
        r2, p2 = pair(200, 'url2', cc=3600)
        r3, p3 = pair(200, 'url3', cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        with pytest.raises(StopIteration):
            sender.send(r1)

        assert sender.send(r2) is p2

    def test_exceeding_max_size_drops_lru_item(self):
        """
        Test if the maximum maximum number of max_size

        Args:
            self: (todo): write your description
        """
        r1, p1 = pair(200, 'url1', cc=3600)
        r2, p2 = pair(200, 'url2', cc=3600)
        r3, p3 = pair(200, 'url3', cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r1)
        sender.send(r3)

        with pytest.raises(StopIteration):
            sender.send(r2)

        assert sender.send(r1) is p1

    def test_cache_size_not_affected_by_stale_other_items(self):
        """
        Test if the cache cache has not already cached.

        Args:
            self: (todo): write your description
        """
        r1, p1 = pair(200, 'url1', cc=3600)
        r2, p2 = pair(200, 'url2', cc=-5)
        r3, p3 = pair(200, 'url3', cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        assert sender.send(r1) is p1
        with pytest.raises(StopIteration):
            sender.send(r2)

    def test_cache_size_not_affected_by_stale_same_items(self):
        """
        The cache of the number of the same size of the same type.

        Args:
            self: (todo): write your description
        """
        r1, p1 = pair(200, 'url1', cc=3600)
        r2, p2 = pair(200, 'url2', cc=-5)
        r3, p3 = pair(200, 'url2', cc=3600)

        sender = CachingSender(sender=mock_sender(p1, p2, p3), max_size=2)
        sender.send(r1)
        sender.send(r2)
        sender.send(r3)

        assert sender.send(r1) is p1
        assert sender.send(r2) is p3
