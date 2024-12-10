from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Coroutine
from dataclasses import dataclass


@dataclass
class Request:
    """Wrapper for parameters of a HTTP request."""

    method: str
    url: str
    params: dict | None = None
    headers: dict | None = None
    data: dict | None = None
    json: dict | None = None
    content: str | None = None


@dataclass
class Response:
    """Wrapper for result of a HTTP request."""

    url: str
    headers: dict
    status_code: int
    content: dict | None


class Sender(ABC):
    """Sender interface for requests."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    @abstractmethod
    def send(self, request: Request) -> Response | Coroutine[None, None, Response]:
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

    @abstractmethod
    def close(self) -> None | Coroutine[None, None, None]:
        """Close underlying client."""
