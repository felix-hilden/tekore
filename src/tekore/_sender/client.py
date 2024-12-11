from __future__ import annotations

from collections.abc import Callable, Coroutine
from functools import wraps
from warnings import warn

from .base import Request, Response
from .concrete import AsyncSender, Sender, SyncSender
from .error import Unauthorised
from .extending import ExtendingSender


class SenderConflictWarning(RuntimeWarning):
    """Sender arguments to a client are in conflict."""


class Client(ExtendingSender):
    """
    Base class for clients.

    Parameters
    ----------
    sender
        request sender - If not specified, a :class:`SyncSender` is used
    asynchronous
        synchronicity requirement - If specified, overrides passed sender
        if they are in conflict and instantiates a sender of the requested type
    """

    def __init__(self, sender: Sender | None, asynchronous: bool | None = None) -> None:
        super().__init__(sender)

        if self.sender.is_async and asynchronous is False:
            self.sender = SyncSender()
        elif not self.sender.is_async and asynchronous is True:
            self.sender = AsyncSender()

        if sender is not None and self.sender.is_async != sender.is_async:
            msg = (
                f"{type(sender)} with is_async={sender.is_async} passed"
                f" but asynchronous={asynchronous}!"
                f"\nA new {type(self.sender).__name__} was instantiated."
            )
            warn(msg, SenderConflictWarning, stacklevel=3)

    def send(self, request: Request) -> Response | Coroutine[None, None, Response]:
        """Send request with underlying sender."""
        return self.sender.send(request)


def send_and_process(post_func: Callable) -> Callable:
    """
    Decorate a Client function to send a request and process its content.

    The first parameter of a decorated function must be the instance (self)
    of a :class:`Sender` (has :meth:`send` and :attr:`is_async`).
    The decorated function must return a tuple with two items:
    a :class:`Request` and a tuple with arguments to unpack to ``post_func``.
    The result of ``post_func`` is returned to the caller.

    Parameters
    ----------
    post_func
        function to call with the request and response
        and possible additional arguments
    """

    def decorator(function: Callable[..., Request]) -> Callable:
        def try_post_func(*args, **kwargs):
            try:
                return post_func(*args, **kwargs)
            except Unauthorised as e:
                e.scope = wrapper.scope
                e.required_scope = wrapper.required_scope
                e.optional_scope = wrapper.optional_scope
                raise

        async def async_send(self: Sender, request: Request, params: tuple):
            response = await self.send(request)
            return try_post_func(request, response, *params)

        @wraps(function)
        def wrapper(self: Sender, *args, **kwargs):
            request, params = function(self, *args, **kwargs)

            if self.is_async:
                return async_send(self, request, params)

            response = self.send(request)
            return try_post_func(request, response, *params)

        return wrapper

    return decorator
