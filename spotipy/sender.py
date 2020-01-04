"""
sender
======
Senders are used to extend the functionality of a client,
that is :class:`client.Spotify`, :class:`auth.Credentials`
and by extension :class:`util.RefreshingCredentials`.

Senders wrap around :class:`requests.Session` providing different levels of
persistence across requests and enabling retries on failed requests.
Here's a short summary of the features of each sender.

- :class:`TransientSender`: Creates a new session for each request (default)
- :class:`PersistentSender`: Reuses a session for requests made on the same instance
- :class:`SingletonSender`: Uses a common session for all instances and requests
- :class:`RetryingSender`: Extends any sender to enable retries on failed requests

Sender instances are passed to a client at initialisation.

.. code:: python

    from spotipy import Spotify, Credentials
    from spotipy.sender import PersistentSender, RetryingSender

    cred = Credentials(
        client_id,
        client_secred,
        redirect_uri,
        sender = PersistentSender()
    )

    sender = RetryingSender(retries=3, sender=PersistentSender())
    spotify = Spotify(sender=sender)

A custom :class:`Session` can be passed in to a sender.

.. code:: python

    from requests import Session
    from spotipy.sender import PresistentSender, SingletonSender

    session = Session()
    session.proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }

    # Attach the session to a sender
    PersistentSender(session)
    SingletonSender.session = session

The default sender can be changed.
Note that this requires importing the whole sender module.

.. code:: python

    from spotipy import sender

    sender.default_sender_type = sender.PersistentSender
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
    Create a new session for each request.
    """
    def send(self, request: Request, **requests_kwargs) -> Response:
        with Session() as sess:
            prepared = sess.prepare_request(request)
            return sess.send(prepared, **requests_kwargs)


class SingletonSender(Sender):
    """
    Use one session for all instances and requests.
    """
    session = Session()

    def send(self, request: Request, **requests_kwargs) -> Response:
        prepared = SingletonSender.session.prepare_request(request)
        return SingletonSender.session.send(prepared, **requests_kwargs)


class PersistentSender(Sender):
    """
    Use a per-instance session to send requests.

    Parameters
    ----------
    session
        :class:`Session` to use when sending requests
    """
    def __init__(self, session: Session = None):
        self.session = session or Session()

    def send(self, request: Request, **requests_kwargs) -> Response:
        prepared = self.session.prepare_request(request)
        return self.session.send(prepared, **requests_kwargs)


default_sender_type = TransientSender   #: Sender to instantiate by default


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
        request sender, :class:`default_sender_type` used if not specified

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
        self.sender = sender or default_sender_type()

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


class Client:
    """
    Base class for clients.

    Parameters
    ----------
    sender
        request sender, :class:`default_sender_type` used if not specified
    requests_kwargs
        keyword arguments for requests.request
    """
    def __init__(self, sender: Sender, requests_kwargs: dict):
        self.sender = sender or default_sender_type()
        self.requests_kwargs = requests_kwargs or {}

    def _send(self, request: Request) -> Response:
        return self.sender.send(request, **self.requests_kwargs)
