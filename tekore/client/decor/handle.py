from requests import Request, Response, HTTPError

from tekore.error import errors
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
        error_cls = errors.get(response.status_code, HTTPError)
        raise error_cls(error_str, request=request, response=response)
