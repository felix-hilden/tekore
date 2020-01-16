import json

from requests import Request, HTTPError

from tekore.sender import Sender, Client, SenderAsync, ClientAsync
from tekore.model.error import PlayerErrorReason

error_format = """Error in {url}:
{code}: {msg}
"""


def parse_json(response):
    try:
        return response.json()
    except ValueError:
        return None


def parse_error_reason(response):
    content = parse_json(response)
    if content is None:
        return response.reason

    error = content['error']
    reason = error.get('message', response.reason)
    if 'reason' in error:
        reason += '\n' + PlayerErrorReason[error['reason']].value
    return reason


class SpotifyBase(Client):
    prefix = 'https://api.spotify.com/v1/'

    def __init__(
            self,
            token=None,
            sender: Sender = None
    ):
        """
        Create a Spotify API object.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender
        """
        super().__init__(sender)
        self.token = token

    def _build_request(self, method: str, url: str, headers: dict = None) -> Request:
        if not url.startswith('http'):
            url = self.prefix + url

        default_headers = {
            'Authorization': f'Bearer {str(self.token)}',
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

    @staticmethod
    def _handle_errors(request, response) -> None:
        if response.status_code >= 400:
            error_str = error_format.format(
                url=response.url,
                code=response.status_code,
                msg=parse_error_reason(response)
            )
            raise HTTPError(error_str, request=request, response=response)

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
        self._handle_errors(request, response)
        return parse_json(response)

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


class SpotifyBaseAsync(ClientAsync):
    prefix = 'https://api.spotify.com/v1/'

    def __init__(
            self,
            token=None,
            sender: SenderAsync = None
    ):
        """
        Create a Spotify API object.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender
        """
        super().__init__(sender)
        self.token = token

    def _build_request(self, method: str, url: str, headers: dict = None) -> Request:
        if not url.startswith('http'):
            url = self.prefix + url

        default_headers = {
            'Authorization': f'Bearer {str(self.token)}',
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

    @staticmethod
    def _handle_errors(request, response) -> None:
        if response.status_code >= 400:
            error_str = error_format.format(
                url=response.url,
                code=response.status_code,
                msg=parse_error_reason(response)
            )
            raise HTTPError(error_str, request=request, response=response)

    async def _request(
            self,
            method: str,
            url: str,
            payload=None,
            params: dict = None
    ):
        request = self._build_request(method, url)
        self._set_content(request, payload, params)
        response = await self._send(request)
        self._handle_errors(request, response)
        return parse_json(response)

    async def _get(self, url: str, payload=None, **params):
        return await self._request('GET', url, payload=payload, params=params)

    async def _post(self, url: str, payload=None, **params):
        return await self._request('POST', url, payload=payload, params=params)

    async def _delete(self, url: str, payload=None, **params):
        return await self._request('DELETE', url, payload=payload, params=params)

    async def _put(self, url: str, payload=None, **params):
        return await self._request('PUT', url, payload=payload, params=params)

    async def _get_paging_result(self, address: str):
        result = await self._get(address)

        # If only one top-level key, the paging object is one level deeper
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]

        return result
