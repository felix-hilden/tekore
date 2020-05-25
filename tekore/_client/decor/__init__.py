from typing import Callable
from warnings import warn
from functools import wraps

from requests import Request
from .handle import handle_errors, parse_json


def send_and_process(post_func: Callable) -> Callable:
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
    def decorator(function: Callable[..., Request]) -> Callable:
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
    doc_msg = f'.. deprecated:: {in_}\n   Removed in {removed}.'
    doc_msg += f'\n   Use :meth:`Spotify.{instead}` instead.'

    err_msg = f'Removed in version {removed}, use Spotify.{instead} instead.'

    def decorator(function: Callable) -> Callable:
        _, head, body = function.__doc__.split('\n', maxsplit=2)
        indent = (len(head) - len(head.lstrip(' '))) * ' '

        nonlocal doc_msg
        doc_msg = indent + doc_msg.replace('\n', '\n' + indent)
        function.__doc__ = '\n'.join([_, head, '', doc_msg, body])

        @wraps(function)
        def wrapper(*args, **kwargs):
            warn(err_msg, DeprecationWarning, stacklevel=level)
            return function(*args, **kwargs)
        return wrapper
    return decorator
