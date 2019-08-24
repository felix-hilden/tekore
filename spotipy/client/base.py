import json
import time
import requests

from contextlib import contextmanager


class SpotifyException(requests.HTTPError):
    def __init__(self, http_status, code, msg, headers=None):
        self.http_status = http_status
        self.code = code
        self.msg = msg

        # `headers` is used to support `Retry-After` in the event
        # of a 429 status code
        if headers is None:
            headers = {}
        self.headers = headers

    def __str__(self):
        return f'http status: {self.http_status},' \
               f' code: {self.code} - {self.msg}'


class SpotifyBase:
    max_get_retries = 10
    prefix = 'https://api.spotify.com/v1/'

    def __init__(self, token: str = None, requests_session=True,
                 requests_kwargs: dict = None):
        """
        Create a Spotify API object.

        Parameters:
            - token - bearer token for requests
            - requests_session - A Requests session object or a truthy value
            to create one. A falsy value disables sessions. It should generally
            be a good idea to keep sessions enabled for performance reasons
            (connection pooling).
            - requests_kwargs - keyword arguments for requests.request
        """
        self._token = token
        self.requests_kwargs = requests_kwargs

        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session:  # Build a new session.
                self._session = requests.Session()
            else:  # Use the Requests API module as a 'session'.
                from requests import api
                self._session = api

    @contextmanager
    def token(self, token: str) -> 'SpotifyBase':
        self._token, old_token = token, self._token
        yield self
        self._token = old_token

    def _internal_call(self, method, url, payload, params):
        if not url.startswith('http'):
            url = self.prefix + url

        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

        params = {k: v for k, v in params.items() if v is not None}

        r = self._session.request(
            method, url,
            headers=headers,
            params=params,
            data=json.dumps(payload) if payload is not None else None,
            **self.requests_kwargs
        )

        try:
            r.raise_for_status()
        except requests.HTTPError as error:
            if r.text and len(r.text) > 0 and r.text != 'null':
                msg = r.json()['error']['message']
            else:
                msg = str(error)
            raise SpotifyException(
                r.status_code, -1, f'{r.url}:\n {msg}', headers=r.headers
            ) from error
        finally:
            r.connection.close()
        if r.text and len(r.text) > 0 and r.text != 'null':
            return r.json()
        else:
            return None

    def _get(self, url, payload=None, **params):
        retries = self.max_get_retries
        delay = 1
        while retries > 0:
            try:
                return self._internal_call('GET', url, payload, params)
            except SpotifyException as e:
                retries -= 1
                status = e.http_status
                # 429 means we hit a rate limit, backoff
                if status == 429 or (500 <= status < 600):
                    if retries < 0:
                        raise
                    else:
                        sleep_seconds = int(e.headers.get('Retry-After',
                                                          delay))
                        print('retrying ...' + str(sleep_seconds) + 'secs')
                        time.sleep(sleep_seconds + 1)
                        delay += 1
                else:
                    raise

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
