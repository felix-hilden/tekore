from httpx import codes

from .base import Request, Response


class HTTPError(Exception):
    """
    Base error for all web status errors.

    Attributes
    ----------
    request
        request that led to the error
    response
        response from the web server
    """

    def __init__(self, message: str, request: Request, response: Response) -> None:
        super().__init__(message)
        self.request = request
        self.response = response


class ClientError(HTTPError):
    """4xx - Base client error."""


class ServerError(HTTPError):
    """5xx - Base server error."""


class BadRequest(ClientError):
    """
    400 - Bad request.

    The request could not be understood by the server due to malformed syntax.
    """


class Unauthorised(ClientError):
    """
    401 - Unauthorised.

    The request requires user authentication or,
    if the request included authorization credentials,
    authorization has been refused for those credentials.

    The scopes associated with the call are attached to this class.
    """

    scope: str
    required_scope: str
    optional_scope: str


class Forbidden(ClientError):
    """
    403 - Forbidden.

    The server understood the request, but is refusing to fulfill it.
    """


class NotFound(ClientError):
    """
    404 - Not found.

    The requested resource could not be found.
    This error can be due to a temporary or permanent condition.
    """


class TooManyRequests(ClientError):
    """
    429 - Too many requests.

    Rate limiting has been applied.
    """


class InternalServerError(ServerError):
    """
    500 - Internal server error.

    You should never receive this error because the clever coders at Spotify
    catch them all... But if you are unlucky enough to get one,
    please report it to Spotify through their GitHub (spotify/web-api).
    """


class BadGateway(ClientError):
    """
    502 - Bad gateway.

    The server was acting as a gateway or proxy and received
    an invalid response from the upstream server.
    """


class ServiceUnavailable(ClientError):
    """
    503 - Service unavailable.

    The server is currently unable to handle the request due to a temporary
    condition which will be alleviated after some delay.
    You can choose to resend the request again.
    """


errors = {
    400: BadRequest,
    401: Unauthorised,
    403: Forbidden,
    404: NotFound,
    429: TooManyRequests,
    500: InternalServerError,
    502: BadGateway,
    503: ServiceUnavailable,
}


def get_error(code: int) -> type[HTTPError]:
    """Get error based on status code or default error."""
    cls = errors.get(code)
    if cls is None:
        cls = ClientError if codes.is_client_error(code) else ServerError
    return cls
