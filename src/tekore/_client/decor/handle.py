from httpx import codes

from tekore._sender import Request, Response
from tekore._sender.error import get_error
from tekore.model import PlayerErrorReason

error_format = """Error in {url}:
{code}: {msg}
"""


def parse_error_reason(response: Response) -> str:
    """Extract error reason from response content."""
    reason = getattr(response, "reason", "")

    if response.content is None:
        return reason

    error = response.content["error"]
    message = error.get("message", reason)
    if "reason" in error:
        message += "\n" + PlayerErrorReason[error["reason"]].value
    return message


def handle_errors(request: Request, response: Response) -> None:
    """Examine response and raise errors accordingly."""
    if codes.is_error(response.status_code):
        error_str = error_format.format(
            url=response.url,
            code=response.status_code,
            msg=parse_error_reason(response),
        )
        error_cls = get_error(response.status_code)
        raise error_cls(error_str, request=request, response=response)
