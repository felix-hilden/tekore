"""
sender
======

Senders are used to extend the Spotify client's functionality.

Senders wrap around :class:`requests.Session` providing different levels of
persistence across requests and enabling retries on failed requests.
Here's a short summary of the features of each sender.

- :class:`TransientSender`: Creates a new session for each request (default)
- :class:`PersistentSender`: Reuses a session for requests made on the same instance
- :class:`SingletonSender`: Uses a global session for all instances and requests
- :class:`RetryingSender`: Extends any sender to enable retries on failed requests

Sender instances are passed to the client at initialisation.

.. code:: python

    from spotipy import Spotify
    from spotipy.sender import PersistentSender, RetryingSender

    sender = RetryingSender(retries=3, sender=PersistentSender())
    spotify = Spotify(sender=sender)
"""

import time

from abc import ABC, abstractmethod
from requests import Request, Response, Session


class Sender(ABC):
    """
    Sender interface for requests.
    """
    @abstractmethod
    def send(self, request: Request, **requests_kwargs) -> Response:
        """
        Prepare and send a request.

        Parameters
        ----------
        request
            requests.Request to send
        requests_kwargs
            keyword arguments for requests.Session.send
        """


class TransientSender(Sender):
    """
    Create a session for each request.
    """
    def send(self, request: Request, **requests_kwargs) -> Response:
        with Session() as sess:
            prepared = sess.prepare_request(request)
            return sess.send(prepared, **requests_kwargs)


class SingletonSender(Sender):
    """
    Use a global session to send requests.
    """
    session = Session()

    def send(self, request: Request, **requests_kwargs) -> Response:
        prepared = SingletonSender.session.prepare_request(request)
        return SingletonSender.session.send(prepared, **requests_kwargs)


class PersistentSender(Sender):
    """
    Use a per-instance session to send requests.
    """
    def __init__(self):
        self.session = Session()

    def send(self, request: Request, **requests_kwargs) -> Response:
        prepared = self.session.prepare_request(request)
        return self.session.send(prepared, **requests_kwargs)


class RetryingSender(Sender):
    """
    Retry requests if unsuccessful.

    On server errors the set amount of retries are used to resend requests.
    On 429 - Too Many Requests the `Retry-After` header is checked and used
    to wait before requesting again.
    Note that even when the number of retries is set to zero,
    retries based on rate limiting are still performed.

    Only holds the retry logic.
    Another sender is used to send requests.

    Parameters
    ----------
    retries
        maximum number of retries on server errors before giving up
    sender
        sender to use when sending requests, TransientSender by default

    Examples
    --------
    Pass the maximum number of retries to retry failed requests.

    .. code:: python

        rs = RetryingSender(retries=3)

    :class:`RetryingSender` can extend any other sender to provide
    the combined functionality.

    .. code:: python

        rs = RetryingSender(sender=SingletonSender())
    """
    def __init__(self, retries: int = 0, sender: Sender = None):
        self.retries = retries
        self.sender = sender or TransientSender()

    def send(self, request: Request, **requests_kwargs) -> Response:
        tries = self.retries + 1
        delay_seconds = 1

        while tries > 0:
            r = self.sender.send(request, **requests_kwargs)

            if r.status_code == 429:
                seconds = r.headers['Retry-After']
                time.sleep(int(seconds))
            elif r.status_code >= 500 and tries > 1:
                tries -= 1
                time.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                return r
