from requests import HTTPError


class BadRequest(HTTPError):
    pass


class Unauthorised(HTTPError):
    pass


class Forbidden(HTTPError):
    pass


class NotFound(HTTPError):
    pass


class TooManyRequests(HTTPError):
    pass


class InternalServerError(HTTPError):
    pass


class BadGateway(HTTPError):
    pass


class ServiceUnavailable(HTTPError):
    pass


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
