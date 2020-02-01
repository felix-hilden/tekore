"""
Manipulate the way clients send requests.

Senders provide different levels of connection persistence across requests
and extend other senders to enable retries on failed requests.
The sender of a :class:`Client` also determines whether synchronous or
asynchronous calls are used to send requests and process responses.
Here's a short summary of the features of each sender.

- :class:`(Async) <AsyncTransientSender>` :class:`TransientSender`:
  Send each request individually (default)
- :class:`(Async) <AsyncPersistentSender>` :class:`PersistentSender`:
  Reuse connections for requests made with one instance
- :class:`(Async) <AsyncSingletonSender>` :class:`SingletonSender`:
  Reuse connections between all instances
- :class:`RetryingSender`: Retry on server errors or hitting the rate limit

Sender instances are passed to a client at initialisation.

.. code:: python

    from tekore import Spotify, Credentials
    from tekore.sender import PersistentSender, AsyncTransientSender

    Credentials(*conf, sender=PersistentSender())
    Spotify(sender=AsyncTransientSender())

Synchronous senders wrap around the :mod:`requests` library,
while asynchronous senders use :mod:`httpx`.
Senders accept additional keyword arguments to :meth:`requests.Session.send`
or :meth:`httpx.AsyncClient.request` that are passed on each request.

.. code:: python

    from tekore.sender import TransientSender

    proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }
    TransientSender(proxies=proxies)

Custom instances of :class:`requests.Session` or :class:`httpx.AsyncClient`
can also be used.

.. code:: python

    from requests import Session
    from tekore.sender import PresistentSender, SingletonSender

    session = Session()
    session.proxies = proxies

    # Attach the session to a sender
    PersistentSender(session)
    SingletonSender.session = session

Default senders and keyword arguments can be changed.
Note that this requires importing the whole sender module.
:attr:`default_sender_instance` has precedence over :attr:`default_sender_type`.
Using a :class:`RetryingSender` as the default type will raise an error
as it tries to instantiate itself recursively.
Use :attr:`default_sender_instance` instead.
See also :attr:`default_httpx_kwargs`.

.. code:: python

    from tekore import sender, Spotify

    sender.default_sender_type = sender.PersistentSender
    sender.default_sender_instance = sender.RetryingSender()
    sender.default_requests_kwargs = {'proxies': proxies}

    # Now the following are equal
    Spotify()
    Spotify(
        sender=sender.RetryingSender(
            sender=sender.PersistentSender(proxies=proxies)
        )
    )
"""

import time
import asyncio

from abc import ABC, abstractmethod
from warnings import warn

from httpx import AsyncClient
from requests import Request, Response, Session


class Sender(ABC):
    """
    Sender interface for requests.
    """
    @abstractmethod
    def send(self, request: Request) -> Response:
        """
        Prepare and send a request.

        Parameters
        ----------
        request
            :class:`Request` to send
        """

    @property
    @abstractmethod
    def is_async(self) -> bool:
        """
        :class:`True` if the sender is asynchronous, :class:`False` otherwise.
        """


default_requests_kwargs = {}
"""
Default keyword arguments to send with in synchronous mode.
Not used when any other keyword arguments are passed in.
"""

default_httpx_kwargs = {}
"""
Default keyword arguments to send with in asynchronous mode.
Not used when any other keyword arguments are passed in.
"""


class SyncSender(Sender, ABC):
    """
    Synchronous request sender base class.
    """
    @property
    def is_async(self) -> bool:
        return False


class AsyncSender(Sender, ABC):
    """
    Asynchronous request sender base class.
    """
    @property
    def is_async(self) -> bool:
        return True


class TransientSender(SyncSender):
    """
    Create a new session for each request.

    Parameters
    ----------
    requests_kwargs
        keyword arguments for :meth:`requests.Session.send`
    """
    def __init__(self, **requests_kwargs):
        self.requests_kwargs = requests_kwargs or default_requests_kwargs

    def send(self, request: Request) -> Response:
        with Session() as sess:
            prepared = sess.prepare_request(request)
            return sess.send(prepared, **self.requests_kwargs)


class AsyncTransientSender(AsyncSender):
    """
    Create a new asynchronous client for each request.

    Parameters
    ----------
    httpx_kwargs
        keyword arguments for :meth:`httpx.AsyncClient.request`
    """
    def __init__(self, **httpx_kwargs):
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs

    async def send(self, request: Request) -> Response:
        async with AsyncClient() as client:
            return await client.request(
                request.method,
                request.url,
                data=request.data or None,
                params=request.params or None,
                headers=request.headers,
                **self.httpx_kwargs,
            )


class SingletonSender(SyncSender):
    """
    Use one session for all instances and requests.

    Parameters
    ----------
    requests_kwargs
        keyword arguments for :meth:`requests.Session.send`
    """
    session = Session()

    def __init__(self, **requests_kwargs):
        self.requests_kwargs = requests_kwargs or default_requests_kwargs

    def send(self, request: Request) -> Response:
        prepared = SingletonSender.session.prepare_request(request)
        return SingletonSender.session.send(prepared, **self.requests_kwargs)


class AsyncSingletonSender(AsyncSender):
    """
    Use one client for all instances and requests.

    Parameters
    ----------
    httpx_kwargs
        keyword arguments for :meth:`httpx.AsyncClient.request`
    """
    client = AsyncClient()

    def __init__(self, **httpx_kwargs):
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs

    async def send(self, request: Request) -> Response:
        return await AsyncSingletonSender.client.request(
            request.method,
            request.url,
            data=request.data or None,
            params=request.params or None,
            headers=request.headers,
            **self.httpx_kwargs,
        )


class PersistentSender(SyncSender):
    """
    Use a per-instance session to send requests.

    Parameters
    ----------
    session
        :class:`requests.Session` to use when sending requests
    requests_kwargs
        keyword arguments for :meth:`requests.Session.send`
    """
    def __init__(self, session: Session = None, **requests_kwargs):
        self.requests_kwargs = requests_kwargs or default_requests_kwargs
        self.session = session or Session()

    def send(self, request: Request) -> Response:
        prepared = self.session.prepare_request(request)
        return self.session.send(prepared, **self.requests_kwargs)


class AsyncPersistentSender(AsyncSender):
    """
    Use a per-instance client to send requests asynchronously.

    Parameters
    ----------
    session
        :class:`httpx.AsyncClient` to use when sending requests
    httpx_kwargs
        keyword arguments for :meth:`httpx.AsyncClient.request`
    """
    def __init__(self, client: AsyncClient = None, **httpx_kwargs):
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs
        self.client = client or AsyncClient()

    async def send(self, request: Request) -> Response:
        async with self.client as client:
            return await client.request(
                request.method,
                request.url,
                data=request.data or None,
                params=request.params or None,
                headers=request.headers,
                **self.httpx_kwargs,
            )


default_sender_type = TransientSender
"""
Sender to instantiate by default.
"""


class RetryingSender(Sender):
    """
    Retry requests if unsuccessful.

    On server errors the set amount of retries are used to resend requests.
    On 429 - Too Many Requests the `Retry-After` header is checked and used
    to wait before requesting again.
    Note that even when the number of retries is set to zero,
    retries based on rate limiting are still performed.

    Only holds the retry logic.
    Another sender is used to send requests.

    Parameters
    ----------
    retries
        maximum number of retries on server errors before giving up
    sender
        request sender, :attr:`default_sender_type` instantiated if not specified

    Examples
    --------
    Pass the maximum number of retries to retry failed requests.

    .. code:: python

        RetryingSender(retries=3)

    :class:`RetryingSender` can extend any other sender to provide
    the combined functionality.

    .. code:: python

        RetryingSender(sender=SingletonSender())
    """
    def __init__(self, retries: int = 0, sender: Sender = None):
        self.retries = retries
        self.sender = sender or default_sender_type()

    @property
    def is_async(self) -> bool:
        return self.sender.is_async

    def send(self, request: Request) -> Response:
        if self.is_async:
            return self._async_send(request)

        tries = self.retries + 1
        delay_seconds = 1

        while tries > 0:
            r = self.sender.send(request)

            if r.status_code == 429:
                seconds = r.headers['Retry-After']
                time.sleep(int(seconds))
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
                seconds = r.headers['Retry-After']
                await asyncio.sleep(int(seconds))
            elif r.status_code >= 500 and tries > 1:
                tries -= 1
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                return r


default_sender_instance = None
"""
Default sender instance to use in clients.
If specified, overrides :attr:`default_sender_type`.
"""


def new_default_sender() -> Sender:
    return default_sender_instance or default_sender_type()


class SenderConflictWarning(RuntimeWarning):
    """Issued when sender arguments to a client are in conflict."""


class Client:
    """
    Base class for clients.

    Parameters
    ----------
    sender
        request sender - If not specified, using :attr:`default_sender_instance`
        is attempted first, then :attr:`default_sender_type` is instantiated.
    asynchronous
        synchronicity requirement - If specified, overrides passed
        sender and defaults if they are in conflict and instantiates
        a transient sender of the requested type
    """
    def __init__(self, sender: Sender, asynchronous: bool = None):
        new_sender = sender or new_default_sender()

        if new_sender.is_async and asynchronous is False:
            new_sender = TransientSender()
        elif not new_sender.is_async and asynchronous is True:
            new_sender = AsyncTransientSender()

        self.sender = new_sender

        if sender is not None and new_sender.is_async != sender.is_async:
            msg = f'\n{type(sender)} passed but asynchronous={asynchronous}!'
            msg += '\nA sender was instantiated according to `asynchronous`.'
            warn(msg, SenderConflictWarning, stacklevel=3)

    def _send(self, request: Request) -> Response:
        return self.sender.send(request)

    @property
    def is_async(self) -> bool:
        return self.sender.is_async
