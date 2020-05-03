from typing import List
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.artist import SimpleArtist
from tekore.model.member import Image, ReleaseDatePrecision
from tekore.model.serialise import StrEnum, ModelList


class AlbumType(StrEnum):
    album = 'album'
    compilation = 'compilation'
    single = 'single'


@dataclass(repr=False)
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
        self.artists = ModelList(SimpleArtist(**a) for a in self.artists)
        self.images = ModelList(Image(**i) for i in self.images)
        self.release_date_precision = ReleaseDatePrecision[
            self.release_date_precision
        ]
