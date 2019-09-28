"""
sender
======

Define request senders to be passed to and used by the Spotify class.

They implement different levels of session usage mainly for connection pooling.
Retries based on rate limiting and server error codes are also available.
Custom subclasses could implement further logic, for example caching.
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
    Send requests and retry if unsuccessful.

    Only the retrying logic is held in RetryingSender.
    Another sender is used to actually send the requests.
    Note that even when the number of retries is set to zero,
    retries based on rate limiting are still performed.

    Parameters
    ----------
    retries
        maximum number of retries on server errors before giving up
    sender
        sender to use when sending requests, TransientSender by default
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
