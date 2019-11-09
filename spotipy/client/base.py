import json

from contextlib import contextmanager
from requests import Request, HTTPError

from spotipy.sender import Sender, TransientSender
from spotipy.model.error import PlayerErrorReason
from spotipy.model.paging import Paging, OffsetPaging

error_format = """Error in {url}:
{code}: {msg}
"""


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
        """
        Access token currently in use.
        """
        return str(self._token)

    @token.setter
    def token(self, value):
        self._token = value

    @contextmanager
    def token_as(self, token) -> 'SpotifyBase':
        """
        Temporarily use a different token with requests.

        Parameters
        ----------
        token
            access token

        Returns
        -------
        SpotifyBase
            self
        """
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
        if payload is not None:
            if request.headers['Content-Type'] == 'application/json':
                request.data = json.dumps(payload)
            else:
                request.data = payload

    def _send(self, request: Request):
        response = self.sender.send(request, **self.requests_kwargs)

        if response.status_code >= 400:
            content = self._parse_json(response)
            error_str = error_format.format(
                url=response.url,
                code=response.status_code,
                msg=content.get('message', None) or response.reason
            )
            if 'reason' in content:
                error_str += '\n' + PlayerErrorReason[content['reason']].value
            raise HTTPError(error_str, request=request, response=response)

        return response

    @staticmethod
    def _parse_json(response):
        try:
            return response.json()
        except ValueError:
            return None

    def _request(
            self,
            method: str,
            url: str,
            payload=None,
            params: dict = None
    ):
        request = self._build_request(method, url)
        self._set_content(request, payload, params)
        response = self._send(request)
        return self._parse_json(response)

    def _get(self, url: str, payload=None, **params):
        return self._request('GET', url, payload=payload, params=params)

    def _post(self, url: str, payload=None, **params):
        return self._request('POST', url, payload=payload, params=params)

    def _delete(self, url: str, payload=None, **params):
        return self._request('DELETE', url, payload=payload, params=params)

    def _put(self, url: str, payload=None, **params):
        return self._request('PUT', url, payload=payload, params=params)

    def _get_paging_result(self, address: str):
        result = self._get(address)

        # If only one top-level key, the paging object is one level deeper
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]

        return result

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
            next_set = self._get_paging_result(result.next)
            return type(result)(**next_set)

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
            previous_set = self._get_paging_result(result.previous)
            return type(result)(**previous_set)
