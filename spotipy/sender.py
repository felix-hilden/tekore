from abc import ABC, abstractmethod
from requests import Request, Response, Session


class Sender(ABC):
    """
    Sender interface for requests.
    """
    @abstractmethod
    def send(self, request: Request, **kwargs) -> Response:
        """
        Prepare and send a request.

        Parameters
        ----------
        request
            requests.Request to send
        kwargs
            keyword arguments for requests.Session.send
        """


class TransientSender(Sender):
    """
    Create a session for each request.
    """
    def send(self, request: Request, **kwargs) -> Response:
        with Session() as sess:
            prepared = sess.prepare_request(request)
            return sess.send(prepared, **kwargs)


class SingletonSender(Sender):
    """
    Use a global session to send requests.
    """
    session = Session()

    def send(self, request: Request, **kwargs) -> Response:
        prepared = SingletonSender.session.prepare_request(request)
        return SingletonSender.session.send(prepared, **kwargs)


class ReusingSender(Sender):
    """
    Use a per-instance session to send requests.
    """
    def __init__(self):
        self.session = Session()

    def send(self, request: Request, **kwargs) -> Response:
        prepared = self.session.prepare_request(request)
        return self.session.send(prepared, **kwargs)
