import time
import asyncio

from abc import ABC
from typing import Optional, Union, Coroutine
from collections import deque
from urllib.parse import urlencode

from .base import Request, Response
from .concrete import Sender, SyncSender


class ExtendingSender(Sender, ABC):
    """
    Base class for senders that extend other senders.

    Parameters
    ----------
    sender
        request sender, :class:`SyncSender` if not specified
    """

    def __init__(self, sender: Optional[Sender]):
        self.sender = sender or SyncSender()

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, delegated to the underlying sender."""
        return self.sender.is_async

    def close(self) -> Union[None, Coroutine[None, None, None]]:
        """
        Close the underlying sender.

        To close synchronous senders, call :meth:`close`.
        To close asynchronous senders, await :meth:`close`.
        """
        return self.sender.close()


class RetryingSender(ExtendingSender):
    """
    Retry requests if unsuccessful.

    On server errors the set amount of retries are used to resend requests.
    On :class:`TooManyRequests` the `Retry-After` header is checked and used
    to wait before requesting again.

    .. note::

        Even when the number of retries is set to zero,
        retries based on rate limiting are still performed.

    Parameters
    ----------
    retries
        maximum number of retries on server errors before giving up
    sender
        request sender, :class:`SyncSender` if not specified

    Examples
    --------
    Use for only rate limiting by leaving the retry count to zero.

    .. code:: python

        tk.RetryingSender()

    Pass the maximum number of retries to retry failed requests.

    .. code:: python

        tk.RetryingSender(retries=3)
    """

    def __init__(self, retries: int = 0, sender: Sender = None):
        super().__init__(sender)
        self.retries = retries

    def __repr__(self):
        contains = f'(retries={self.retries}, sender={self.sender!r})'
        return type(self).__name__ + contains

    def send(
        self, request: Request
    ) -> Union[Response, Coroutine[None, None, Response]]:
        """Delegate request to underlying sender and retry if failed."""
        if self.is_async:
            return self._async_send(request)

        tries = self.retries + 1
        delay_seconds = 1

        while tries > 0:
            r = self.sender.send(request)

            if r.status_code == 429:
                seconds = r.headers.get('Retry-After', 1)
                time.sleep(int(seconds) + 1)
            elif r.status_code >= 500 and tries > 1:
                tries -= 1
                time.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                return r

    async def _async_send(self, request: Request) -> Response:
        tries = self.retries + 1
        delay_seconds = 1

        while tries > 0:
            r = await self.sender.send(request)

            if r.status_code == 429:
                seconds = r.headers.get('Retry-After', 1)
                await asyncio.sleep(int(seconds) + 1)
            elif r.status_code >= 500 and tries > 1:
                tries -= 1
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                return r


class CachingSender(ExtendingSender):
    """
    Cache successful GET requests.

    The Web API provides response headers for caching.
    Resources are cached based on Cache-Control, ETag and Vary headers.
    Thus :class:`CachingSender` can be used with user tokens too.
    Resources marked as private, errors and ``Vary: *`` are not cached.

    When using asynchronous senders, the cache is protected with
    :class:`asyncio.Lock` to prevent concurrent access.
    The lock is instantiated on the first asynchronous call,
    so using only one :func:`asyncio.run` (per sender) is advised.

    Note that if the cache has no maximum size it can grow without limit.
    Use :meth:`CachingSender.clear` to empty the cache.

    Parameters
    ----------
    max_size
        maximum cache size (amount of responses), if specified the least
        recently used response is discarded when the cache would overflow
    sender
        request sender, :class:`SyncSender` if not specified
    """

    def __init__(self, max_size: int = None, sender: Sender = None):
        super().__init__(sender)
        self._max_size = max_size
        self._cache = {}
        self._deque = deque(maxlen=self.max_size)
        self._lock: Optional[asyncio.Lock] = None

    def __repr__(self):
        contains = f'(max_size={self._max_size}, sender={self.sender!r})'
        return type(self).__name__ + contains

    @property
    def max_size(self) -> Optional[int]:
        """
        Maximum amount of requests stored in the cache.

        Returns
        -------
        Optional[int]
            maximum cache size
        """
        return self._max_size

    def clear(self) -> None:
        """Clear sender cache."""
        self._cache = {}
        self._deque.clear()

    @staticmethod
    def _vary_key(request: Request, vary: Optional[list]):
        if vary is not None:
            return ' '.join(request.headers[k] for k in vary)

    @staticmethod
    def _cc_fresh(item: dict) -> bool:
        return item['expires_at'] > time.time()

    @staticmethod
    def _has_etag(item: dict) -> bool:
        return item['etag'] is not None

    def _is_fresh(self, url, vary_key) -> bool:
        item = self._cache[url][1][vary_key]
        return self._cc_fresh(item) or self._has_etag(item)

    def _delete(self, url, vary_key) -> None:
        item = self._cache[url]
        del item[1][vary_key]
        if not item[1]:
            del item

    def _maybe_save(self, request: Request, response: Response) -> None:
        cc = response.headers.get('Cache-Control', 'private, max-age=0')

        if response.status_code >= 400 or 'private' in cc:
            return

        age = int(cc.split('max-age=')[1].split(',')[0])
        vary = response.headers.get('Vary', None)
        if vary is not None:
            if '*' in vary:
                return
            vary = vary.split(', ')

        # Construct cached response
        cache_item = self._cache.get(response.url, (vary, {}))
        self._cache[response.url] = cache_item

        cached_response = {
            'response': response,
            'expires_at': time.time() + age - 1,
            'etag': response.headers.get('ETag', None),
        }
        vary_key = self._vary_key(request, vary)
        cache_item[1].update({vary_key: cached_response})

        # Manage cache size
        if self.max_size is None:
            return

        # Remove stale items
        if len(self._deque) == self._deque.maxlen:
            deque_items = list(self._deque)
            self._deque.clear()

            for item in deque_items:
                fresh = self._is_fresh(*item)

                if fresh:
                    self._deque.append(item)
                else:
                    self._delete(*item)

        # Remove LRU item
        if len(self._deque) == self._deque.maxlen:
            d_url, d_vary_key = self._deque.popleft()
            self._delete(d_url, d_vary_key)

        self._deque.append((response.url, vary_key))

    def _update_usage(self, item) -> None:
        if self.max_size is None:
            return

        self._deque.remove(item)
        self._deque.append(item)

    def _load(self, request: Request) -> tuple:
        params = ('&' + urlencode(request.params)) if request.params else ''
        url = request.url + params
        item = self._cache.get(url, None)

        if item is None:
            return None, None

        vary_key = self._vary_key(request, item[0])
        cached = item[1].get(vary_key, None)

        if cached is not None:
            response = cached['response']
            deque_item = (url, vary_key)
            if self._cc_fresh(cached):
                self._update_usage(deque_item)
                return response, None
            elif self._has_etag(cached):
                self._update_usage(deque_item)
                return response, cached['etag']
            elif self.max_size is not None:
                self._deque.remove(deque_item)

        return None, None

    def _handle_fresh(self, request, fresh: Response, cached: Response):
        if fresh.status_code == 304:
            return cached
        else:
            self._maybe_save(request, fresh)
            return fresh

    def send(
        self, request: Request
    ) -> Union[Response, Coroutine[None, None, Response]]:
        """Maybe load request from cache, or delegate to underlying sender."""
        if self.is_async:
            return self._async_send(request)

        if request.method.lower() != 'get':
            return self.sender.send(request)

        cached, etag = self._load(request)
        if cached is not None and etag is None:
            return cached
        elif etag is not None:
            request.headers.update(ETag=etag)

        fresh = self.sender.send(request)
        return self._handle_fresh(request, fresh, cached)

    async def _async_send(self, request: Request):
        if request.method.lower() != 'get':
            return await self.sender.send(request)

        if self._lock is None:
            self._lock = asyncio.Lock()

        async with self._lock:
            cached, etag = self._load(request)

        if cached is not None and etag is None:
            return cached
        elif etag is not None:
            request.headers.update(ETag=etag)

        fresh = await self.sender.send(request)
        async with self._lock:
            return self._handle_fresh(request, fresh, cached)
