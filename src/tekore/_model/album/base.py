from __future__ import annotations

from ..artist import SimpleArtist
from ..base import Item
from ..member import Image, ReleaseDatePrecision
from ..serialise import StrEnum


class AlbumType(StrEnum):
    """Type of album."""

    album = "album"
    compilation = "compilation"
    single = "single"
    ep = "ep"


class Album(Item):
    """Album base."""

    album_type: AlbumType
    artists: list[SimpleArtist]
    external_urls: dict
    images: list[Image]
    name: str
    total_tracks: int
    release_date: str
    release_date_precision: ReleaseDatePrecision
    available_markets: list[str] | None = None
    is_playable: bool | None = None
