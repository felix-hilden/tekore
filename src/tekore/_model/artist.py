from typing import List

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
    genres: List[str]
    images: List[Image]
    popularity: int


class FullArtistCursorPaging(CursorPaging):
    """Paging of full artists."""

    items: List[FullArtist]
    total: int


class FullArtistOffsetPaging(OffsetPaging):
    """Paging of full artists."""

    items: List[FullArtist]
