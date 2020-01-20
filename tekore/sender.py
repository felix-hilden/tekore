"""
Manipulate the way clients send requests.

Senders wrap around :class:`requests.Session` providing different levels of
persistence across requests and enabling retries on failed requests.
Additionally, keyword arguments accepted by Requests and
custom :class:`Session` instances can be passed in too.
Here's a short summary of the features of each sender.

- :class:`TransientSender`: Create a new session for each request (default)
- :class:`PersistentSender`: Reuse a session for requests made on the same instance
- :class:`SingletonSender`: Use a common session for all instances and requests
- :class:`RetryingSender`: Extend any sender to enable retries on failed requests

Sender instances are passed to a client at initialisation.

.. code:: python

    from tekore import Spotify, Credentials
    from tekore.sender import PersistentSender, RetryingSender

    cred = Credentials(
        client_id,
        client_secred,
        redirect_uri,
        sender = PersistentSender()
    )

    sender = RetryingSender(retries=3, sender=PersistentSender())
    spotify = Spotify(sender=sender)

Keyword arguments accepted by Requests can be passed into senders.

.. code:: python

    from tekore.sender import TransientSender

    proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }
    TransientSender(proxies=proxies)

A custom :class:`Session` can also be used.

.. code:: python

    from requests import Session
    from tekore.sender import PresistentSender, SingletonSender

    session = Session()
    session.proxies = proxies

    # Attach the session to a sender
    PersistentSender(session)
    SingletonSender.session = session

The default senders and keyword arguments can be changed.
Note that this requires importing the whole sender module.
:attr:`default_sender_instance` has precedence over :attr:`default_sender_type`.
Using a :class:`RetryingSender` as the default type will raise an error
as it tries to instantiate itself recursively.
Use :attr:`default_sender_instance` instead.

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

from abc import ABC, abstractmethod
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


class AsyncSender(Sender, ABC):
    """
    Asynchronous request sender base class.
    """


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
        synchronous request sender, :attr:`default_sender_type`
        instantiated if not specified

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
    def __init__(self, retries: int = 0, sender: SyncSender = None):
        self.retries = retries
        self.sender = sender or default_sender_type()

    def send(self, request: Request) -> Response:
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


default_sender_instance = None
"""
Default sender instance to use in clients.
If specified, overrides :attr:`default_sender_type`.
"""


class Client:
    """
    Base class for clients.

    Parameters
    ----------
    sender
        request sender - If not specified, using :attr:`default_sender_instance`
        is attempted first, then :attr:`default_sender_type` is instantiated.
    """
    def __init__(self, sender: Sender):
        self.sender = sender or default_sender_instance or default_sender_type()

    def _send(self, request: Request) -> Response:
        return self.sender.send(request)

    @property
    def is_async(self) -> bool:
        return isinstance(self.sender, AsyncSender)
