import json

from contextlib import contextmanager
from requests import Request, HTTPError

from spotipy.sender import Sender, TransientSender
from spotipy.model import Paging, OffsetPaging


class SpotifyBase:
    prefix = 'https://api.spotify.com/v1/'

    def __init__(
            self,
            token=None,
            sender: Sender = None,
            requests_kwargs: dict = None
    ):
        """
        Create a Spotify API object.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender, TransientSender by default
        requests_kwargs
            keyword arguments for requests.request
        """
        self._token = token
        self.requests_kwargs = requests_kwargs or {}
        self.sender = sender or TransientSender()

    @property
    def token(self):
        return str(self._token)

    @token.setter
    def token(self, value):
        self._token = value

    @contextmanager
    def token_as(self, token) -> 'SpotifyBase':
        self._token, old_token = token, self.token
        yield self
        self._token = old_token

    def _build_request(self, method: str, url: str, headers: dict = None) -> Request:
        if not url.startswith('http'):
            url = self.prefix + url

        default_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        default_headers.update(headers or {})

        return Request(method, url, headers=default_headers)

    @staticmethod
    def _set_content(request: Request, payload=None, params: dict = None) -> None:
        params = params or {}
        request.params = {k: v for k, v in params.items() if v is not None}
        request.data = json.dumps(payload) if payload is not None else None

    def _send(self, request: Request):
        r = self.sender.send(request, **self.requests_kwargs)

        if r.status_code >= 400:
            raise HTTPError(f'Error ({r.status_code}) in {r.url}', request=r)

        return r

    def _get(self, url: str, payload=None, **params):
        request = self._build_request('GET', url)
        self._set_content(request, payload, params)
        response = self._send(request)

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return None

    def _post(self, url: str, payload=None, **params):
        r = self._build_request('POST', url)
        self._set_content(r, payload, params)
        self._send(r)

    def _delete(self, url: str, payload=None, **params):
        r = self._build_request('DELETE', url)
        self._set_content(r, payload, params)
        self._send(r)

    def _put(self, url: str, payload=None, **params):
        r = self._build_request('PUT', url)
        self._set_content(r, payload, params)
        self._send(r)

    def next(self, result: Paging) -> Paging:
        """
        Retrieve the next result set of a paging object.

        Parameters
        ----------
        result
            paging object

        Returns
        -------
        Paging
            paging object containing the next result set
        """
        if result.next is not None:
            return type(result)(**self._get(result.next))

    def previous(self, result: OffsetPaging) -> OffsetPaging:
        """
        Retrieve the previous result set of a paging object.

        Parameters
        ----------
        result
            offset-based paging object

        Returns
        -------
        OffsetPaging
            paging object containing the previous result set
        """
        if result.previous is not None:
            return type(result)(**self._get(result.previous))
