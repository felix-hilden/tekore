import json
import time
import requests

from contextlib import contextmanager


class SpotifyException(requests.HTTPError):
    pass


class SpotifyBase:
    prefix = 'https://api.spotify.com/v1/'

    def __init__(self, token: str = None, session=True, retries: int = 0,
                 requests_kwargs: dict = None):
        """
        Create a Spotify API object.

        Parameters:
            - token - bearer token for requests
            - session - requests session object or a truthy value
            to create one. A falsy value disables sessions. It should generally
            be a good idea to keep sessions enabled for connection pooling.
            - retries - maximum number of retries on a failed request
            - requests_kwargs - keyword arguments for requests.request
        """
        self._token = token
        self.retries = retries
        self.requests_kwargs = requests_kwargs or {}

        if isinstance(session, requests.Session):
            self._session = session
        else:
            if session:  # Build a new session.
                self._session = requests.Session()
            else:  # Use the Requests API module as a 'session'.
                from requests import api
                self._session = api

    @contextmanager
    def token(self, token: str) -> 'SpotifyBase':
        self._token, old_token = token, self._token
        yield self
        self._token = old_token

    def _request(self, method: str, url: str, headers: dict = None,
                 params: dict = None, data=None):
        retries = self.retries + 1
        delay = 1

        while retries > 0:
            r = self._session.request(
                method, url,
                headers=headers,
                params=params,
                data=data,
                **self.requests_kwargs
            )

            if 200 <= r.status_code < 400:
                return r
            elif r.status_code == 429 or r.status_code >= 500:
                retries -= 1
                if retries < 0:
                    raise SpotifyException(
                        f'Maximum number of retries exceeded!\n'
                        f'{r.url}: {r.status_code}'
                    )

                seconds = int(r.headers.get('Retry-After', delay))
                time.sleep(seconds)
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

        r = self._request(
            method, url,
            headers=headers,
            params={k: v for k, v in params.items() if v is not None},
            data=json.dumps(payload) if payload is not None else None
        )

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
