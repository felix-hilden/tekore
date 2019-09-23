from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.paging import CursorPaging, OffsetPaging
from spotipy.model.member import Followers, Image


@dataclass
class Artist(Item):
    external_urls: dict
    name: str


@dataclass
class SimpleArtist(Artist):
    pass


@dataclass
class FullArtist(Artist):
    followers: Followers
    genres: List[str]
    images: List[Image]
    popularity: int

    def __post_init__(self):
        self.followers = Followers(**self.followers)
        self.images = [Image(**i) for i in self.images]


@dataclass
class FullArtistCursorPaging(CursorPaging):
    items: List[FullArtist]

    def __post_init__(self):
        self.items = [FullArtist(**a) for a in self.items]


@dataclass
class FullArtistOffsetPaging(OffsetPaging):
    items: List[FullArtist]

    def __post_init__(self):
        self.items = [FullArtist(**a) for a in self.items]
