from typing import List, Literal, Union

from pydantic import Field

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
    available_markets: List[None] = Field(default_factory=list)
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
    :attr:`duration_ms` being an object is undocumented.
    """

    album: LocalAlbum
    artists: List[LocalArtist]
    available_markets: List[None] = Field(default_factory=list)
    disc_number: int
    duration_ms: Union[int, dict]
    explicit: bool
    external_ids: dict
    external_urls: dict
    is_local: Literal[True]
    popularity: int
    preview_url: None
    track_number: int
    uri: str
