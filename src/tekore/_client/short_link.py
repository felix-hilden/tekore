from httpx import codes

from tekore._sender import Request, Response, send_and_process
from tekore._sender.base import Sender

from .base import SpotifyBase


def is_short_link(url: str) -> bool:
    """Determine if URL is a Spotify short link."""
    return "spotify.link/" in url


def _process_short_link(request: Request, response: Response) -> str:
    if response.status_code == codes.TEMPORARY_REDIRECT:
        return response.headers["location"]
    return request.url


@send_and_process(_process_short_link)
def _send_short_link(_: Sender, request: tuple[Request, tuple]) -> str:
    return request


class SpotifyShortLink(SpotifyBase):
    """Spotify short link."""

    def follow_short_link(self, link: str) -> str:
        """
        Follow redirect of a short link to get the underlying resource URL.

        Safely also accept a direct link, request a redirect and return
        the original URL. Also use the underlying sender for an unauthenticated request.

        Returns
        -------
        url
            result of the short link redirect
        """
        request = self._request("HEAD", link)
        return _send_short_link(self.sender, request)
