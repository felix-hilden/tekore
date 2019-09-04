import json
import time
import requests

from contextlib import contextmanager
from spotipy.sender import Sender, TransientSender


class SpotifyException(requests.HTTPError):
    pass


class SpotifyBase:
    prefix = 'https://api.spotify.com/v1/'

    def __init__(self, token: str = None, sender: Sender = None, retries: int = 0,
                 requests_kwargs: dict = None):
        """
        Create a Spotify API object.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender. If None, a default sender is created
        retries
            maximum number of retries on a failed request
        requests_kwargs
            keyword arguments for requests.request
        """
        self._token = token
        self.retries = retries
        self.requests_kwargs = requests_kwargs or {}
        self.sender = sender or TransientSender()

    @contextmanager
    def token(self, token: str) -> 'SpotifyBase':
        self._token, old_token = token, self._token
        yield self
        self._token = old_token

    def _send(self, request: requests.Request):
        retries = self.retries + 1
        delay = 1

        while retries > 0:
            r = self.sender.send(request, **self.requests_kwargs)

            if 200 <= r.status_code < 400:
                return r
            elif r.status_code == 429:
                seconds = r.headers['Retry-After']
                time.sleep(int(seconds))
            elif r.status_code >= 500:
                retries -= 1
                if retries == 0:
                    raise SpotifyException(
                        f'Maximum number of retries exceeded!\n'
                        f'{r.url}: {r.status_code}'
                    )

                time.sleep(delay)
                delay *= 2
            else:
                if r.text and len(r.text) > 0 and r.text != 'null':
                    msg = f'{r.status_code} - {r.json()["error"]["message"]}'
                else:
                    msg = f'Status code: {r.status_code}'
                raise SpotifyException(
                    f'Error in {r.url}:\n{msg}'
                )

    def _internal_call(self, method, url, payload, params):
        if not url.startswith('http'):
            url = self.prefix + url

        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

        request = requests.Request(
            method, url,
            headers=headers,
            params={k: v for k, v in params.items() if v is not None},
            data=json.dumps(payload) if payload is not None else None
        )
        r = self._send(request)

        if r.text and len(r.text) > 0:
            return r.json()
        else:
            return None

    def _get(self, url, payload=None, **params):
        return self._internal_call('GET', url, payload, params)

    def _post(self, url, payload=None, **params):
        return self._internal_call('POST', url, payload, params)

    def _delete(self, url, payload=None, **params):
        return self._internal_call('DELETE', url, payload, params)

    def _put(self, url, payload=None, **params):
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
