from enum import Enum
from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.artist import SimpleArtist
from spotipy.model.member import ExternalURL, Image, Restrictions

AlbumType = Enum('AlbumType', 'album single compilation')
ReleaseDatePrecision = Enum('ReleaseDatePrecision', 'year month day')


@dataclass
class Album(Item):
    album_type: AlbumType
    artists: List[SimpleArtist]
    available_markets: List[str]
    external_urls: ExternalURL
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: ReleaseDatePrecision
    restrictions: Restrictions
