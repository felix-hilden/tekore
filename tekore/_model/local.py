from typing import List
from dataclasses import dataclass

from .serialise import Model, ModelList


@dataclass(repr=False)
class LocalItem(Model):
    """Base for local items."""

    id: None
    href: None
    name: str
    type: str
    uri: None


@dataclass(repr=False)
class LocalAlbum(LocalItem):
    """Album of a locally saved track."""

    album_type: None
    artists: List[None]
    available_markets: List[None]
    external_urls: dict
    images: List[None]
    release_date: None
    release_date_precision: None


@dataclass(repr=False)
class LocalArtist(LocalItem):
    """Artist of a locally saved track."""

    external_urls: dict


@dataclass(repr=False)
class LocalTrack(LocalItem):
    """
    Locally saved track.

    Locally saved track where most attributes are
    always None, empty, zero or False.
    """

    album: LocalAlbum
    artists: List[LocalArtist]
    available_markets: List[None]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: dict
    external_urls: dict
    is_local: bool
    popularity: int
    preview_url: None
    track_number: int
    uri: str

    def __post_init__(self):
        self.album = LocalAlbum(**self.album)
        self.artists = ModelList(LocalArtist(**a) for a in self.artists)
