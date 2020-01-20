import json

from functools import wraps
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
    return {k: v for k, v in params.items() if v is not None} or None


def parse_json(response):
    try:
        return response.json()
    except ValueError:
        return None


def parse_error_reason(response):
    content = parse_json(response)
    reason = getattr(response, 'reason', '')

    if content is None:
        return reason

    error = content['error']
    message = error.get('message', reason)
    if 'reason' in error:
        message += '\n' + PlayerErrorReason[error['reason']].value
    return message


def handle_errors(request: Request, response: Response) -> None:
    if response.status_code >= 400:
        error_str = error_format.format(
            url=response.url,
            code=response.status_code,
            msg=parse_error_reason(response)
        )
        raise HTTPError(error_str, request=request, response=response)


def send_and_process(post_func: callable) -> callable:
    """
    Decorate a function to send a request and process its content.

    The first parameter of a decorated function must be the instance (self)
    of a client with a :meth:`_send` method.
    The instance must also have :attr:`is_async`, based on which a synchronous
    or an asynchronous function is used in the process.
    The decorated function must return a :class:`requests.Request`.
    The result of ``post_func`` is returned to the caller.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    """
    def decorator(function: callable) -> callable:
        async def async_send(self, request: Request):
            response = await self._send(request)
            handle_errors(request, response)
            content = parse_json(response)
            return post_func(content)

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            request = function(self, *args, **kwargs)

            if self.is_async:
                return async_send(self, request)

            response = self._send(request)
            handle_errors(request, response)
            content = parse_json(response)
            return post_func(content)
        return wrapper
    return decorator


class SpotifyBase(Client):
    def __init__(
            self,
            token=None,
            sender: Sender = None,
            asynchronous: bool = None,
    ):
        """
        Client to Web API endpoints.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender
        asynchronous
            synchronicity requirement
        """
        super().__init__(sender, asynchronous)
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
        return Request(
            method=method,
            url=build_url(url),
            headers=self._create_headers(),
            params=parse_url_params(params),
            data=json.dumps(payload) if payload is not None else None
        )

    def _get(self, url: str, payload=None, **params):
        return self._request('GET', url, payload=payload, params=params)

    def _post(self, url: str, payload=None, **params):
        return self._request('POST', url, payload=payload, params=params)

    def _delete(self, url: str, payload=None, **params):
        return self._request('DELETE', url, payload=payload, params=params)

    def _put(self, url: str, payload=None, **params):
        return self._request('PUT', url, payload=payload, params=params)
