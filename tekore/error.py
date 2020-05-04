"""
Web exceptions for :mod:`auth <tekore.auth>` and :mod:`client <tekore.client>`.

Clients facing the Web API raise errors when recieving bad status codes.
Specific errors or all web errors can be caught.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    token = tk.request_client_token(*conf[:2])
    spotify = tk.Spotify(token)

    try:
        spotify.album('not-a-real-album')
    except tk.BadRequest:
        print('Whoops, bad request!')
    except tk.HTTPError:
        print('How did you get here?')
"""

import requests


class HTTPError(requests.HTTPError):
    """
    Base error for all web errors.
    """


class BadRequest(HTTPError):
    """
    400 - Bad request

    The request could not be understood by the server due to malformed syntax.
    """


class Unauthorised(HTTPError):
    """
    401 - Unauthorised

    The request requires user authentication or,
    if the request included authorization credentials,
    authorization has been refused for those credentials.
    """


class Forbidden(HTTPError):
    """
    403 - Forbidden

    The server understood the request, but is refusing to fulfill it.
    """


class NotFound(HTTPError):
    """
    404 - Not found

    The requested resource could not be found.
    This error can be due to a temporary or permanent condition.
    """


class TooManyRequests(HTTPError):
    """
    429 - Too many requests

    Rate limiting has been applied.
    """


class InternalServerError(HTTPError):
    """
    500 - Internal server error

    You should never receive this error because the clever coders at Spotify
    catch them all... But if you are unlucky enough to get one,
    please report it to Spotify through their GitHub (spotify/web-api).
    """


class BadGateway(HTTPError):
    """
    502 - Bad gateway

    The server was acting as a gateway or proxy and received
    an invalid response from the upstream server.
    """


class ServiceUnavailable(HTTPError):
    """
    503 - Service unavailable

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
