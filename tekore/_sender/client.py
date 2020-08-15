from typing import Optional, Union, Coroutine
from warnings import warn

from .base import Request, Response
from .concrete import Sender, SyncSender, AsyncSender
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

    def __init__(self, sender: Optional[Sender], asynchronous: bool = None):
        super().__init__(sender)

        if self.sender.is_async and asynchronous is False:
            self.sender = SyncSender()
        elif not self.sender.is_async and asynchronous is True:
            self.sender = AsyncSender()

        if sender is not None and self.sender.is_async != sender.is_async:
            msg = (
                f'{type(sender)} with is_async={sender.is_async} passed'
                f' but asynchronous={asynchronous}!'
                f'\nA new {type(self.sender).__name__} was instantiated.'
            )
            warn(msg, SenderConflictWarning, stacklevel=3)

    def send(
        self, request: Request
    ) -> Union[Response, Coroutine[None, None, Response]]:
        """Send request with underlying sender."""
        return self.sender.send(request)
