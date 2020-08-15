from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union, Coroutine


@dataclass
class Request:
    """Wrapper for parameters of a HTTP request."""

    method: str
    url: str
    params: Optional[dict] = None
    headers: Optional[dict] = None
    data: Union[str, dict, None] = None


@dataclass
class Response:
    """Wrapper for result of a HTTP request."""

    url: str
    headers: dict
    status_code: int
    content: Optional[dict]


class Sender(ABC):
    """Sender interface for requests."""

    @abstractmethod
    def send(
        self,
        request: Request
    ) -> Union[Response, Coroutine[None, None, Response]]:
        """
        Send a request.

        Parameters
        ----------
        request
            request to send

        Returns
        -------
        Response
            resulting response
        """

    @property
    @abstractmethod
    def is_async(self) -> bool:
        """Sender asynchronicity mode."""
