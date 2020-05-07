from typing import Optional
from warnings import warn
from requests import Request, Response

from .concrete import Sender, PersistentSender, AsyncPersistentSender


def new_default_sender() -> Sender:
    from tekore import default_sender_instance, default_sender_type
    return default_sender_instance or default_sender_type()


class SenderConflictWarning(RuntimeWarning):
    """
    Sender arguments to a client are in conflict.
    """


class Client:
    """
    Base class for clients.

    Parameters
    ----------
    sender
        request sender - If not specified, using :attr:`default_sender_instance`
        is attempted first, then :attr:`default_sender_type` is instantiated.
    asynchronous
        synchronicity requirement - If specified, overrides passed
        sender and defaults if they are in conflict and instantiates
        a persistent sender of the requested type
    """
    def __init__(self, sender: Optional[Sender], asynchronous: bool = None):
        new_sender = sender or new_default_sender()

        if new_sender.is_async and asynchronous is False:
            new_sender = PersistentSender()
        elif not new_sender.is_async and asynchronous is True:
            new_sender = AsyncPersistentSender()

        self.sender = new_sender

        if sender is not None and new_sender.is_async != sender.is_async:
            msg = f'\n{type(sender)} passed but asynchronous={asynchronous}!'
            msg += '\nA sender was instantiated according to `asynchronous`.'
            warn(msg, SenderConflictWarning, stacklevel=3)

    def _send(self, request: Request) -> Response:
        return self.sender.send(request)

    @property
    def is_async(self) -> bool:
        return self.sender.is_async
