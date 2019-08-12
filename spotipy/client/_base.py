import sys
import json
import time
import requests

from contextlib import contextmanager


class SpotifyException(Exception):
    def __init__(self, http_status, code, msg, headers=None):
        self.http_status = http_status
        self.code = code
        self.msg = msg

        # `headers` is used to support `Retry-After` in the event of a 429 status code
        if headers is None:
            headers = {}
        self.headers = headers

    def __str__(self):
        return 'http status: {0}, code:{1} - {2}'.format(
            self.http_status, self.code, self.msg)


class SpotifyBase:
    max_get_retries = 10
    prefix = 'https://api.spotify.com/v1/'

    def __init__(self, requests_session=True, proxies=None, requests_timeout=None):
        """
        Create a Spotify API object.

        :param requests_session:
            A Requests session object or a truthy value to create one.
            A falsy value disables sessions.
            It should generally be a good idea to keep sessions enabled
            for performance reasons (connection pooling).
        :param proxies:
            Definition of proxies (optional)
        :param requests_timeout:
            Tell Requests to stop waiting for a response after a given number of seconds
        """
        self._token = None
        self.proxies = proxies
        self.requests_timeout = requests_timeout

        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session:  # Build a new session.
                self._session = requests.Session()
            else:  # Use the Requests API module as a "session".
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
            'Authorization': 'Bearer {0}'.format(self._token),
            'Content-Type': 'application/json'
        }

        args = {
            'params': {k: v for k, v in params.items() if v is not None},
            'timeout': self.requests_timeout
        }
        if payload:
            args["data"] = json.dumps(payload)

        r = self._session.request(method, url, headers=headers, proxies=self.proxies, **args)

        try:
            r.raise_for_status()
        except requests.HTTPError:
            if r.text and len(r.text) > 0 and r.text != 'null':
                raise SpotifyException(
                    r.status_code, -1, '%s:\n %s' % (r.url, r.json()['error']['message']), headers=r.headers
                )
            else:
                raise SpotifyException(r.status_code, -1, '%s:\n %s' % (r.url, 'error'), headers=r.headers)
        finally:
            r.connection.close()
        if r.text and len(r.text) > 0 and r.text != 'null':
            return r.json()
        else:
            return None

    def _get(self, url, payload=None, **kwargs):
        retries = self.max_get_retries
        delay = 1
        while retries > 0:
            try:
                return self._internal_call('GET', url, payload, kwargs)
            except SpotifyException as e:
                retries -= 1
                status = e.http_status
                # 429 means we hit a rate limit, backoff
                if status == 429 or (500 <= status < 600):
                    if retries < 0:
                        raise
                    else:
                        sleep_seconds = int(e.headers.get('Retry-After', delay))
                        print('retrying ...' + str(sleep_seconds) + 'secs')
                        time.sleep(sleep_seconds + 1)
                        delay += 1
                else:
                    raise

    def _post(self, url, payload=None, **kwargs):
        return self._internal_call('POST', url, payload, kwargs)

    def _delete(self, url, payload=None, **kwargs):
        return self._internal_call('DELETE', url, payload, kwargs)

    def _put(self, url, payload=None, **kwargs):
        return self._internal_call('PUT', url, payload, kwargs)

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

    @staticmethod
    def _warn(msg, *args):
        print('warning:' + msg.format(*args), file=sys.stderr)

    def _get_id(self, type_: str, id_: str):
        fields = id_.split(':')
        if len(fields) >= 3:
            if type_ != fields[-2]:
                self._warn('expected id of type %s but found type %s %s', type_, fields[-2], id_)
            return fields[-1]

        fields = id_.split('/')
        if len(fields) >= 3:
            itype = fields[-2]
            if type_ != itype:
                self._warn('expected id of type %s but found type %s %s', type_, itype, id_)
            return fields[-1]
        return id_

    def _get_uri(self, type_: str, id_: str):
        return 'spotify:' + type_ + ":" + self._get_id(type_, id_)
