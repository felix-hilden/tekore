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

    .. warning::

        The underlying client is *not* closed automatically.
        Use :code:`sender.client.close()` to close it,
        particularly if multiple senders are instantiated.

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
            json=request.json,
            content=request.content,
        )
        return Response(
            url=str(response.url),
            headers=response.headers,
            status_code=response.status_code,
            content=try_parse_json(response),
        )

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`False`."""
        return False

    def close(self) -> None:
        """Close the underlying synchronous client."""
        return self.client.close()


class AsyncSender(Sender):
    """
    Send requests asynchronously.

    .. warning::

        The underlying client is **not** closed automatically.
        Use :code:`await sender.client.aclose()` to close it,
        particularly if multiple senders are instantiated.

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
            json=request.json,
            content=request.content,
        )
        return Response(
            url=str(response.url),
            headers=response.headers,
            status_code=response.status_code,
            content=try_parse_json(response),
        )

    @property
    def is_async(self) -> bool:
        """Sender asynchronicity, always :class:`True`."""
        return True

    async def close(self) -> None:
        """Close the underlying asynchronous client."""
        return await self.client.aclose()
