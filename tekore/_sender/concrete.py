from asyncio import ensure_future
from typing import Optional
from httpx import Client, AsyncClient, Response as HTTPXResponse

from .base import Sender, Request, Response


def try_parse_json(response: HTTPXResponse) -> Optional[dict]:
    """Parse json content or return None if not successful."""
    try:
        return response.json()
    except ValueError:
        return None


class SyncSender(Sender):
    """
    Send requests synchronously.

    .. note:: :attr:`client` is closed when the sender is deleted.

    Parameters
    ----------
    client
        :class:`httpx.Client` to use when sending requests
    """

    def __init__(self, client: Client = None):
        self.client = client or Client()

    def send(self, request: Request) -> Response:
        """Send request with :class:`httpx.Client`."""
        response = self.client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            data=request.data,
        )
        return Response(
            url=str(response.url),
            headers=response.headers,
            status_code=response.status_code,
            content=try_parse_json(response),
        )

    def __del__(self):
        self.client.close()

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`False`."""
        return False


class AsyncSender(Sender):
    """
    Send requests asynchronously.

    .. note:: :attr:`client` is closed when the sender is deleted.

    Parameters
    ----------
    client
        :class:`httpx.AsyncClient` to use when sending requests
    """

    def __init__(self, client: AsyncClient = None):
        self.client = client or AsyncClient()

    async def send(self, request: Request) -> Response:
        """Send request with :class:`httpx.AsyncClient`."""
        response = await self.client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            data=request.data,
        )
        return Response(
            url=str(response.url),
            headers=response.headers,
            status_code=response.status_code,
            content=try_parse_json(response),
        )

    async def _close(self):
        await self.client.aclose()

    def __del__(self):
        ensure_future(self._close())

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`True`."""
        return True
