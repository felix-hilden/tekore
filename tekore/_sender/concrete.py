from abc import ABC, abstractmethod
from httpx import AsyncClient
from requests import Request, Response, Session


class Sender(ABC):
    """Sender interface for requests."""

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
        """Sender asynchronicity mode."""


class SyncSender(Sender, ABC):
    """Synchronous request sender base class."""

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`False`."""
        return False


class AsyncSender(Sender, ABC):
    """Asynchronous request sender base class."""

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`True`."""
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
        from tekore import default_requests_kwargs
        self.requests_kwargs = requests_kwargs or default_requests_kwargs

    def send(self, request: Request) -> Response:
        """Send request with new session."""
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
        from tekore import default_httpx_kwargs
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs

    async def send(self, request: Request) -> Response:
        """Send request with new client."""
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
        from tekore import default_requests_kwargs
        self.requests_kwargs = requests_kwargs or default_requests_kwargs

    def send(self, request: Request) -> Response:
        """Send request with global session."""
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
        from tekore import default_httpx_kwargs
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs

    async def send(self, request: Request) -> Response:
        """Send request with global client."""
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
        from tekore import default_requests_kwargs
        self.requests_kwargs = requests_kwargs or default_requests_kwargs
        self.session = session or Session()

    def send(self, request: Request) -> Response:
        """Send request with instance session."""
        prepared = self.session.prepare_request(request)
        return self.session.send(prepared, **self.requests_kwargs)

    def __del__(self):
        self.session.close()


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
        from tekore import default_httpx_kwargs
        self.httpx_kwargs = httpx_kwargs or default_httpx_kwargs
        self.client = client or AsyncClient()

    async def send(self, request: Request) -> Response:
        """Send request with instance client."""
        return await self.client.request(
            request.method,
            request.url,
            data=request.data or None,
            params=request.params or None,
            headers=request.headers,
            **self.httpx_kwargs,
        )
