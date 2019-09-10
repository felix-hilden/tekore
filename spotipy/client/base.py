import json

from contextlib import contextmanager
from requests import Request, HTTPError
from spotipy.sender import Sender, TransientSender


class SpotifyBase:
    prefix = 'https://api.spotify.com/v1/'

    def __init__(
            self,
            token: str = None,
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

    @contextmanager
    def token(self, token: str) -> 'SpotifyBase':
        self._token, old_token = token, self._token
        yield self
        self._token = old_token

    def _internal_call(self, method: str, url: str, payload, params: dict):
        if not url.startswith('http'):
            url = self.prefix + url

        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

        request = Request(
            method, url,
            headers=headers,
            params={k: v for k, v in params.items() if v is not None},
            data=json.dumps(payload) if payload is not None else None
        )
        r = self.sender.send(request, **self.requests_kwargs)

        if r.status_code >= 400:
            raise HTTPError(f'Error ({r.status_code}) in {r.url}', request=r)

        if r.text and len(r.text) > 0:
            return r.json()
        else:
            return None

    def _get(self, url: str, payload=None, **params):
        return self._internal_call('GET', url, payload, params)

    def _post(self, url: str, payload=None, **params):
        return self._internal_call('POST', url, payload, params)

    def _delete(self, url: str, payload=None, **params):
        return self._internal_call('DELETE', url, payload, params)

    def _put(self, url: str, payload=None, **params):
        return self._internal_call('PUT', url, payload, params)

    def next(self, result):
        if result['next']:
            return self._get(result['next'])
        else:
            return None

    def previous(self, result):
        if result['previous']:
            return self._get(result['previous'])
        else:
            return None
