import json

from requests import Request, Response, HTTPError

from tekore.sender import Sender, Client
from tekore.model.error import PlayerErrorReason

prefix = 'https://api.spotify.com/v1/'
error_format = """Error in {url}:
{code}: {msg}
"""


def build_url(url: str) -> str:
    if not url.startswith('http'):
        url = prefix + url
    return url


def parse_url_params(params: dict = None) -> dict:
    params = params or {}
    return {k: v for k, v in params.items() if v is not None}


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


def handle_errors(request: Request, response: Response) -> None:
    if response.status_code >= 400:
        error_str = error_format.format(
            url=response.url,
            code=response.status_code,
            msg=parse_error_reason(response)
        )
        raise HTTPError(error_str, request=request, response=response)


class SpotifyBase(Client):
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
        request = Request(
            method=method,
            url=build_url(url),
            headers=self._create_headers(),
            params=parse_url_params(params),
            data=json.dumps(payload) if payload is not None else None
        )
        response = self._send(request)
        handle_errors(request, response)
        return parse_json(response)

    def _get(self, url: str, payload=None, **params):
        return self._request('GET', url, payload=payload, params=params)

    def _post(self, url: str, payload=None, **params):
        return self._request('POST', url, payload=payload, params=params)

    def _delete(self, url: str, payload=None, **params):
        return self._request('DELETE', url, payload=payload, params=params)

    def _put(self, url: str, payload=None, **params):
        return self._request('PUT', url, payload=payload, params=params)
