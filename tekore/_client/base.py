import json

from typing import Optional, Union, Coroutine
from contextvars import ContextVar
from tekore._sender import Sender, Client, Request, Response

prefix = 'https://api.spotify.com/v1/'


def build_url(url: str) -> str:
    """Attach API address to endpoint."""
    if not url.startswith('http'):
        url = prefix + url
    return url


def parse_url_params(params: Optional[dict]) -> Optional[dict]:
    """Generate parameter dict and filter Nones."""
    params = params or {}
    return {k: v for k, v in params.items() if v is not None} or None


class SpotifyBase(Client):
    """Base client with options and utility functions."""

    _token_cv = ContextVar('_token_cv')
    _max_limits_on_cv = ContextVar('_max_limits_on_cv')
    _chunked_on_cv = ContextVar('_chunked_on_cv')

    def __init__(
            self,
            token=None,
            sender: Sender = None,
            asynchronous: bool = None,
            max_limits_on: bool = False,
            chunked_on: bool = False,
    ):
        # Docstring in the main client
        super().__init__(sender, asynchronous)
        self._token = token
        self._max_limits_on = max_limits_on
        self._chunked_on = chunked_on

    @property
    def token(self):
        """Token getter."""
        return self._token_cv.get(self._token)

    @token.setter
    def token(self, value):
        try:
            self._token_cv.get()
        except LookupError:
            self._token = value
        else:
            self._token_cv.set(value)

    @property
    def max_limits_on(self):
        """Max limits getter."""
        return self._max_limits_on_cv.get(self._max_limits_on)

    @max_limits_on.setter
    def max_limits_on(self, value):
        try:
            self._max_limits_on_cv.get()
        except LookupError:
            self._max_limits_on = value
        else:
            self._max_limits_on_cv.set(value)

    @property
    def chunked_on(self):
        """Chunked getter."""
        return self._chunked_on_cv.get(self._chunked_on)

    @chunked_on.setter
    def chunked_on(self, value):
        try:
            self._chunked_on_cv.get()
        except LookupError:
            self._chunked_on = value
        else:
            self._chunked_on_cv.set(value)

    def __repr__(self):
        options = [
            f'token={self.token!r}',
            f'max_limits_on={self.max_limits_on}',
            f'chunked_on={self.chunked_on}',
            f'sender={self.sender!r}',
        ]
        return type(self).__name__ + '(' + ', '.join(options) + ')'

    def _create_headers(self, content_type: str = 'application/json'):
        return {
            'Authorization': f'Bearer {str(self.token)}',
            'Content-Type': content_type
        }

    def send(
        self, request: Request
    ) -> Union[Response, Coroutine[None, None, Response]]:
        """
        Build request url and headers, and send with underlying sender.

        Exposed to easily send arbitrary requests,
        for custom behavior in some endpoint e.g. for a subclass.
        It may also come in handy if a bugfix or a feature is not implemented
        in a timely manner, or in debugging related to the client or Web API.
        """
        request.url = build_url(request.url)
        headers = self._create_headers()
        if request.headers is not None:
            headers.update(request.headers)
        request.headers = headers
        return self.sender.send(request)

    @staticmethod
    def _request(
            method: str,
            url: str,
            payload: dict = None,
            params: dict = None
    ):
        return Request(
            method=method,
            url=url,
            params=parse_url_params(params),
            json=payload,
        ), ()

    def _get(self, url: str, payload: dict = None, **params):
        return self._request('GET', url, payload=payload, params=params)

    def _post(self, url: str, payload: dict = None, **params):
        return self._request('POST', url, payload=payload, params=params)

    def _delete(self, url: str, payload: dict = None, **params):
        return self._request('DELETE', url, payload=payload, params=params)

    def _put(self, url: str, payload: dict = None, **params):
        return self._request('PUT', url, payload=payload, params=params)
