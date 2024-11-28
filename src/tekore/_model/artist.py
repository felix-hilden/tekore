from .base import Item
from .member import Followers, Image
from .paging import CursorPaging, OffsetPaging


class Artist(Item):
    """Artist base."""

    external_urls: dict
    name: str


class SimpleArtist(Artist):
    """Simplified artist object."""


class FullArtist(Artist):
    """Complete artist object."""

    followers: Followers
    genres: list[str]
    images: list[Image]
    popularity: int


class FullArtistCursorPaging(CursorPaging):
    """Paging of full artists."""

    items: list[FullArtist]
    total: int


class FullArtistOffsetPaging(OffsetPaging):
    """Paging of full artists."""

    items: list[FullArtist]
