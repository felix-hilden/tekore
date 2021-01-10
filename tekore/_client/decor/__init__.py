from typing import Callable
from functools import wraps

from .handle import handle_errors
from tekore._auth import Scope
from tekore._sender import send_and_process as _send_and_process


def send_and_process(post_func: Callable) -> Callable:
    """
    Decorate a Spotify endpoint to send a request and process its content.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    """
    def parse_response(request, response):
        handle_errors(request, response)
        return post_func(response.content)

    return _send_and_process(parse_response)


def maximise_limit(max_limit: int) -> Callable:
    """
    Decorate a function to maximise the value of a 'limit' argument.

    Parameters
    ----------
    max_limit
        maximum value of the limit
    """
    def decorator(function: Callable) -> Callable:
        varnames = function.__code__.co_varnames
        arg_pos = varnames.index('limit') - 1

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if self.max_limits_on and len(args) <= arg_pos:
                kwargs.setdefault('limit', max_limit)
            return function(self, *args, **kwargs)
        return wrapper
    return decorator


def _add_doc_section(doc: str, section: str) -> str:
    """Add section with correct indentation to docstring."""
    items = doc.split('\n', maxsplit=2)

    if len(items) == 1:
        empty = ''
        head = items[0]
        body = ''
    else:
        empty, head, body = items

    indent = (len(head) - len(head.lstrip(' '))) * ' '

    section = indent + section.replace('\n', '\n' + indent)
    return '\n'.join([empty, head, '', section, body])


def scopes(required: list = None, optional: list = None) -> Callable:
    """
    List the scopes that a call uses.

    Provides ``required_scopes``, ``optional_scopes``
    and their combination ``scopes``.
    Also modifies the docstring to include scope information.

    Parameters
    ----------
    required
        required scopes
    optional
        optional scopes
    """
    required = required or []
    optional = optional or []
    required_scope = Scope(*required)
    optional_scope = Scope(*optional)
    doc_msg = '\n'.join([
        '| Required :class:`scope`: ' + (str(required_scope) or 'none'),
        '| Optional :class:`scope`: ' + (str(optional_scope) or 'none')
    ])

    def decorator(function: Callable) -> Callable:
        function.required_scope = required_scope
        function.optional_scope = optional_scope
        function.scope = required_scope + optional_scope
        function.__doc__ = _add_doc_section(function.__doc__, doc_msg)
        return function
    return decorator
