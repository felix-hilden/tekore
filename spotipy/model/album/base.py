from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableEnum
from spotipy.model.base import Item
from spotipy.model.artist import SimpleArtist
from spotipy.model.member import Image


class AlbumType(SerialisableEnum):
    album = 'album'
    compilation = 'compilation'
    single = 'single'


class ReleaseDatePrecision(SerialisableEnum):
    year = 'year'
    month = 'month'
    day = 'day'


@dataclass
class Album(Item):
    album_type: AlbumType
    artists: List[SimpleArtist]
    external_urls: dict
    images: List[Image]
    name: str
    total_tracks: int
    release_date: str
    release_date_precision: ReleaseDatePrecision

    def __post_init__(self):
        self.album_type = AlbumType[self.album_type.lower()]
        self.artists = [SimpleArtist(**a) for a in self.artists]
        self.images = [Image(**i) for i in self.images]
        self.release_date_precision = ReleaseDatePrecision[
            self.release_date_precision
        ]
