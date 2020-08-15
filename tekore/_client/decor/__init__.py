from typing import Callable
from warnings import warn
from functools import wraps

from .handle import handle_errors
from tekore._auth import Scope
from tekore._sender import Request


def send_and_process(post_func: Callable) -> Callable:
    """
    Decorate a function to send a request and process its content.

    The first parameter of a decorated function must be the instance (self)
    of a :class:`Sender` (has :meth:`send` and :attr:`is_async`).
    The result of ``post_func`` is returned to the caller.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    """
    def decorator(function: Callable[..., Request]) -> Callable:
        async def async_send(self, request: Request):
            response = await self.send(request)
            handle_errors(request, response)
            return post_func(response.content)

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            request = function(self, *args, **kwargs)

            if self.is_async:
                return async_send(self, request)

            response = self.send(request)
            handle_errors(request, response)
            return post_func(response.content)
        return wrapper
    return decorator


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


def deprecated(in_: str, removed: str, instead: str, level: int = 2):
    """
    Inject deprecation notice to :class:`Spotify` methods.

    Parameters
    ----------
    in_
        deprecated in version
    removed
        removed in version
    instead
        use this instead
    level
        warning stacklevel
    """
    doc_msg = '\n'.join([
        f'.. deprecated:: {in_}',
        f'   Removed in {removed}.',
        f'   Use :meth:`Spotify.{instead}` instead.'
    ])

    err_msg = f'Removed in version {removed}, use Spotify.{instead} instead.'

    def decorator(function: Callable) -> Callable:
        function.__doc__ = _add_doc_section(function.__doc__, doc_msg)

        @wraps(function)
        def wrapper(*args, **kwargs):
            warn(err_msg, DeprecationWarning, stacklevel=level)
            return function(*args, **kwargs)
        return wrapper
    return decorator


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
