from dataclasses import dataclass
from typing import List

from ..artist import SimpleArtist
from ..base import Item
from ..member import Image, ReleaseDatePrecision
from ..serialise import ModelList, StrEnum


class AlbumType(StrEnum):
    """Type of album."""

    album = "album"
    compilation = "compilation"
    single = "single"


@dataclass(repr=False)
class Album(Item):
    """Album base."""

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
        self.artists = ModelList(SimpleArtist.from_kwargs(a) for a in self.artists)
        self.images = ModelList(Image.from_kwargs(i) for i in self.images)
        self.release_date_precision = ReleaseDatePrecision[self.release_date_precision]
