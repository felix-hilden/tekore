from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.member import ExternalURL, Followers, Image


@dataclass
class Artist(Item):
    external_urls: ExternalURL
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
