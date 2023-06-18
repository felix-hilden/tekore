from typing import List, Literal

from .serialise import Model


class LocalItem(Model):
    """Base for local items."""

    id: None
    href: None
    name: str
    type: str
    uri: None


class LocalAlbum(LocalItem):
    """Album of a locally saved track."""

    album_type: None
    artists: List[None]
    available_markets: List[None]
    external_urls: dict
    images: List[None]
    release_date: None
    release_date_precision: None


class LocalArtist(LocalItem):
    """Artist of a locally saved track."""

    external_urls: dict


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
    is_local: Literal[True]
    popularity: int
    preview_url: None
    track_number: int
    uri: str
