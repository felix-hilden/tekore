import json

from typing import Type, Optional

from requests import Request, HTTPError

from tekore.sender import Sender, Client
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


def set_content(request: Request, payload=None, params: dict = None) -> None:
    params = params or {}
    request.params = {k: v for k, v in params.items() if v is not None}
    if payload is not None:
        if request.headers['Content-Type'] == 'application/json':
            request.data = json.dumps(payload)
        else:
            request.data = payload


def handle_errors(request, response) -> None:
    if response.status_code >= 400:
        error_str = error_format.format(
            url=response.url,
            code=response.status_code,
            msg=parse_error_reason(response)
        )
        raise HTTPError(error_str, request=request, response=response)


def process_response(request, response, cast_type: Optional[Type] = None):
    handle_errors(request, response)
    parsed = parse_json(response)
    if cast_type is None:
        return parsed
    
    return cast_type(**parsed)


def process_paging_object(paging: dict, cast_type: Type):
    # If only one top-level key, the paging object is one level deeper
    if len(paging) == 1:
        key = list(paging.keys())[0]
        paging = paging[key]

    return cast_type(**paging)

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

    def _request(
            self,
            method: str,
            url: str,
            payload=None,
            params: dict = None,
            cast_type: Optional[Type] = None,
    ):
        request = self._build_request(method, url)
        set_content(request, payload, params)
        # If async sender - return Awaitable
        if self.is_async:
            return self.__request(request, cast_type)

        response = self._send(request)
        return process_response(request, response, cast_type)

    async def __request(self, request: Request, cast_type: Optional[Type] = None):
        response = await self._send(request)
        return process_response(request, response, cast_type)

    def _get(self, url: str, payload=None, cast_type: Optional[Type] = None, **params):
        return self._request(
            'GET',
            url,
            payload=payload,
            params=params,
            cast_type=cast_type
        )

    def _post(self, url: str, payload=None, cast_type: Optional[Type] = None, **params):
        return self._request(
            'POST',
            url,
            payload=payload,
            params=params,
            cast_type=cast_type
        )

    def _delete(self, url: str, payload=None, cast_type: Optional[Type] = None, **params):
        return self._request(
            'DELETE',
            url,
            payload=payload,
            params=params,
            cast_type=cast_type
        )

    def _put(self, url: str, payload=None, cast_type: Optional[Type] = None, **params):
        return self._request(
            'PUT',
            url,
            payload=payload,
            params=params,
            cast_type=cast_type
        )

    def _get_paging_result(self, address: str, cast_type: Type):
        # If async sender - return Awaitable
        if self.is_async:
            return self.__get_paging_result(address, cast_type)

        return process_paging_object(self._get(address), cast_type)
    
    async def __get_paging_result(self, address: str, cast_type: Type):
        return process_paging_object(await self._get(address), cast_type)
