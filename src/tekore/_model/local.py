from __future__ import annotations

from typing import Literal

from pydantic import Field

from .serialise import Model


class LocalItem(Model):
    """Base for local items."""

    id: None
    href: None
    name: str
    type: str


class LocalAlbum(LocalItem):
    """Album of a locally saved track."""

    album_type: None
    artists: list[None]
    available_markets: list[None] = Field(default_factory=list)
    external_urls: dict
    images: list[None]
    release_date: None
    release_date_precision: None
    uri: None


class LocalArtist(LocalItem):
    """Artist of a locally saved track."""

    external_urls: dict
    uri: None


class LocalTrack(LocalItem):
    """
    Locally saved track.

    Locally saved track where most attributes are
    always None, empty, zero or False.
    :attr:`duration_ms` being an object is undocumented.
    """

    album: LocalAlbum
    artists: list[LocalArtist]
    available_markets: list[None] = Field(default_factory=list)
    disc_number: int
    duration_ms: int | dict
    explicit: bool
    external_ids: dict
    external_urls: dict
    is_local: Literal[True]
    popularity: int
    preview_url: None
    track_number: int
    uri: str
