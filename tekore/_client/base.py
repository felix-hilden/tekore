import json

from typing import Optional
from requests import Request

from tekore._sender import Sender, Client

prefix = 'https://api.spotify.com/v1/'


def build_url(url: str) -> str:
    if not url.startswith('http'):
        url = prefix + url
    return url


def parse_url_params(params: Optional[dict]) -> Optional[dict]:
    params = params or {}
    return {k: v for k, v in params.items() if v is not None} or None


class SpotifyBase(Client):
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
        self.token = token
        self.max_limits_on = max_limits_on
        self.chunked_on = chunked_on

    def _create_headers(self, content_type: str = 'application/json'):
        return {
            'Authorization': f'Bearer {str(self.token)}',
            'Content-Type': content_type
        }

    def _request(
            self,
            method: str,
            url: str,
            payload=None,
            params: dict = None
    ):
        return Request(
            method=method,
            url=build_url(url),
            headers=self._create_headers(),
            params=parse_url_params(params),
            data=json.dumps(payload) if payload is not None else None
        )

    def _get(self, url: str, payload=None, **params):
        return self._request('GET', url, payload=payload, params=params)

    def _post(self, url: str, payload=None, **params):
        return self._request('POST', url, payload=payload, params=params)

    def _delete(self, url: str, payload=None, **params):
        return self._request('DELETE', url, payload=payload, params=params)

    def _put(self, url: str, payload=None, **params):
        return self._request('PUT', url, payload=payload, params=params)
