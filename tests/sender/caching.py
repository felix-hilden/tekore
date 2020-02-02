from asyncio import run
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

from tekore.sender import CachingSender
from tests._util import AsyncMock


def mock_sender(*responses, is_async: bool = False):
    sender = MagicMock()
    sender.is_async = is_async
    if is_async:
        sender.send = AsyncMock(side_effect=responses)
    else:
        sender.send.side_effect = responses
    return sender


def request(url, params, headers) -> MagicMock:
    r = MagicMock()
    r.method = 'GET'
    r.url = url
    r.params = params
    r.headers = headers
    return r


def response(code, url, params, cc=None, etag=None, vary=None) -> MagicMock:
    r = MagicMock()
    r.status_code = code
    r.url = url + ('&' + urlencode(params) if params else '')
    if isinstance(cc, int):
        cc = f'public, max-age={cc}'
    h = {
        'Cache-Control': cc,
        'ETag': etag,
        'Vary': vary
    }
    r.headers = {k: v for k, v in h.items() if v is not None}
    return r


def pair(code, url, params=None, cc=None, etag=None, vary_h=None) -> MagicMock:
    req = request(url, params or {}, vary_h or {})
    if vary_h is not None:
        vary = ', '.join([k for k in vary_h])
    else:
        vary = None
    res = response(code, url, params or {}, cc, etag, vary)
    return req, res


def multiple(func: callable, n: int, *args, **kwargs):
    return [func(*args, **kwargs) for _ in range(n)]


class TestCachingSender(TestCase):
    def setUp(self):
        self.sender = CachingSender()

    def test_other_methods_than_GET_not_cached(self):
        methods = ('PUT', 'POST', 'DELETE')

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, '', {}) for _ in requests]
            self.sender.sender = mock_sender(*responses)
            sent = [self.sender.send(r) for r in requests]
            with self.subTest(f'Method {meth} not cached'):
                self.assertIsNot(sent[0], sent[1])

    def test_async_other_methods_not_cached(self):
        methods = ('PUT', 'POST', 'DELETE')

        for meth in methods:
            requests = [MagicMock(), MagicMock()]
            requests[0].method = meth
            requests[1].method = meth

            responses = [response(200, '', {}) for _ in requests]
            self.sender.sender = mock_sender(*responses, is_async=True)
            sent = [run(self.sender.send(r)) for r in requests]
            with self.subTest(f'Method {meth} not cached'):
                self.assertIsNot(sent[0], sent[1])

    def test_params_affect_cache_url(self):
        r1, p1 = pair(200, 'url', cc=10)
        r2, p2 = pair(200, 'url', {'p': 1}, cc=10)

        self.sender.sender = mock_sender(p1, p2)
        self.sender.send(r1)
        self.sender.send(r2)
        with self.subTest(f'Without params'):
            self.assertIs(self.sender.send(r1), p1)
        with self.subTest(f'With params'):
            self.assertIs(self.sender.send(r2), p2)

    def test_vary_affects_caching(self):
        r1, p1 = pair(200, 'url', cc=10, vary_h={'h': 'a'})
        r2, p2 = pair(200, 'url', cc=10, vary_h={'h': 'b'})

        self.sender.sender = mock_sender(p1, p2)
        self.sender.send(r1)
        self.sender.send(r2)
        with self.subTest(f'First vary'):
            self.assertIs(self.sender.send(r1), p1)
        with self.subTest(f'Second vary'):
            self.assertIs(self.sender.send(r2), p2)

    def assert_two_sent(self, r, p1, p2):
        self.sender.sender = mock_sender(p1, p2)
        self.sender.send(r)
        self.assertIs(self.sender.send(r), p2)

    def test_error_not_cached(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 400, 'url', {}, cc=10)
        self.assert_two_sent(r, p1, p2)

    def test_vary_star_not_cached(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10, vary='*')
        self.assert_two_sent(r, p1, p2)

    def test_cc_private_not_cached(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc='private, max-age=0')
        self.assert_two_sent(r, p1, p2)

    def test_no_cc_and_no_etag_not_cached(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {})
        self.assert_two_sent(r, p1, p2)

    def test_no_cc_and_has_etag_not_cached(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, etag='a')
        self.assert_two_sent(r, p1, p2)

    def test_private_cc_and_has_etag_not_cached(self):
        r = request('url', {}, {})
        cc = 'private, max-age=0'
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=cc, etag='a')
        self.assert_two_sent(r, p1, p2)

    def test_has_cc_and_no_etag_is_cached(self):
        r = request('url', {}, {})
        p = response(200, 'url', {}, cc=10)

        self.sender.sender = mock_sender(p)
        self.sender.send(r)
        self.assertIs(self.sender.send(r), p)

    def test_async_has_cc_and_no_etag_is_cached(self):
        r = request('url', {}, {})
        p = response(200, 'url', {}, cc=10)

        self.sender.sender = mock_sender(p, is_async=True)
        run(self.sender.send(r))
        self.assertIs(run(self.sender.send(r)), p)

    def test_cc_only_new_returned_when_stale(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        self.sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15])
        with patch('tekore.sender.time.time', time):
            self.sender.send(r)
            self.assertIs(self.sender.send(r), p2)

    def test_cc_only_stale_replaced_with_new(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        self.sender.sender = mock_sender(p1, p2)
        time = MagicMock(side_effect=[0, 15, 15, 20])
        with patch('tekore.sender.time.time', time):
            self.sender.send(r)
            self.sender.send(r)
            self.assertIs(self.sender.send(r), p2)

    def test_etag_only_cached_returned_on_304(self):
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(304, 'url', {})

        time = MagicMock(side_effect=[0, 15, 15])
        with patch('tekore.sender.time.time', time):
            self.sender.sender = mock_sender(p1, p2)
            self.sender.send(r)
            with self.subTest('Returns cached'):
                self.assertIs(self.sender.send(r), p1)
            with self.subTest('ETag used'):
                self.assertIn('ETag', r.headers)

    def test_etag_only_fresh_returned_on_success(self):
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15])
        with patch('tekore.sender.time.time', time):
            self.sender.sender = mock_sender(p1, p2)
            self.sender.send(r)
            with self.subTest('Returns cached'):
                self.assertIs(self.sender.send(r), p2)
            with self.subTest('ETag used'):
                self.assertIn('ETag', r.headers)

    def test_async_etag_only_fresh_returned_on_success(self):
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15])
        with patch('tekore.sender.time.time', time):
            self.sender.sender = mock_sender(p1, p2, is_async=True)
            run(self.sender.send(r))
            with self.subTest('Returns cached'):
                self.assertIs(run(self.sender.send(r)), p2)
            with self.subTest('ETag used'):
                self.assertIn('ETag', r.headers)

    def test_etag_only_stale_replaced_with_new(self):
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=0, etag='a')
        p2 = response(200, 'url', {}, cc=0, etag='b')
        p3 = response(304, 'url', {}, cc=0, etag='b')

        time = MagicMock(side_effect=[0, 15, 15, 30, 30])
        with patch('tekore.sender.time.time', time):
            self.sender.sender = mock_sender(p1, p2, p3)
            self.sender.send(r)
            self.sender.send(r)
            self.assertIs(self.sender.send(r), p2)

    def test_fresh_cc_precedes_etag(self):
        r = request('url', {}, {})
        p1 = response(200, 'url', {}, cc=10, etag='a')
        p2 = response(304, 'url', {})

        time = MagicMock(side_effect=[0, 15])
        with patch('tekore.sender.time.time', time):
            self.sender.sender = mock_sender(p1, p2)
            self.sender.send(r)
            self.assertIs(self.sender.send(r), p1)

    def test_clear(self):
        r = request('url', {}, {})
        p1, p2 = multiple(response, 2, 200, 'url', {}, cc=10)

        self.sender.sender = mock_sender(p1, p2)
        self.sender.send(r)
        self.sender.clear()
        self.assertIs(self.sender.send(r), p2)
