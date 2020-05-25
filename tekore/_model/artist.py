from typing import List
from dataclasses import dataclass

from .base import Item
from .paging import CursorPaging, OffsetPaging
from .member import Followers, Image
from .serialise import ModelList


@dataclass(repr=False)
class Artist(Item):
    """Artist base."""

    external_urls: dict
    name: str


@dataclass(repr=False)
class SimpleArtist(Artist):
    """Simplified artist object."""


@dataclass(repr=False)
class FullArtist(Artist):
    """Complete artist object."""

    followers: Followers
    genres: List[str]
    images: List[Image]
    popularity: int

    def __post_init__(self):
        self.followers = Followers(**self.followers)
        self.genres = ModelList(self.genres)
        self.images = ModelList(Image(**i) for i in self.images)


@dataclass(repr=False)
class FullArtistCursorPaging(CursorPaging):
    """Paging of full artists."""

    items: List[FullArtist]
    total: int

    def __post_init__(self):
        super().__post_init__()
        self.items = ModelList(FullArtist(**a) for a in self.items)


@dataclass(repr=False)
class FullArtistOffsetPaging(OffsetPaging):
    """Paging of full artists."""

    items: List[FullArtist]

    def __post_init__(self):
        self.items = ModelList(FullArtist(**a) for a in self.items)
