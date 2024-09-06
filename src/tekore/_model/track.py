from datetime import datetime
from typing import List, Optional

from .album import SimpleAlbum
from .artist import SimpleArtist
from .base import Item
from .member import Restrictions
from .paging import OffsetPaging
from .serialise import Model


class TrackLink(Item):
    """Relinked track."""

    external_urls: dict


class Track(Item):
    """Track base."""

    artists: List[SimpleArtist]
    available_markets: Optional[List[str]] = None
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: dict
    is_local: bool
    is_playable: Optional[bool] = None
    linked_from: Optional[TrackLink] = None
    name: str
    preview_url: Optional[str] = None
    restrictions: Optional[Restrictions] = None
    track_number: int


class SimpleTrack(Track):
    """
    Simplified track object.

    When market is specified, :attr:`available_markets` is not available.
    :attr:`is_playable` is not available when market is not specified.
    :attr:`restrictions` is available if restrictions have been placed on
    the track, making it unplayable.
    """


class FullTrack(Track):
    """
    Complete track object.

    When market is specified, :attr:`available_markets` is not available.
    :attr:`is_playable` is not available when market is not specified.
    :attr:`restrictions` is available if restrictions have been placed on
    the track, making it unplayable.
    """

    album: SimpleAlbum
    external_ids: dict
    popularity: int


class FullTrackPaging(OffsetPaging):
    """Paging of full tracks."""

    items: List[FullTrack]


class SimpleTrackPaging(OffsetPaging):
    """Paging of simplified tracks."""

    items: List[SimpleTrack]


class Tracks(Model):
    """Minimal representation of playlist tracks."""

    href: str
    total: int


class SavedTrack(Model):
    """Track saved to library."""

    added_at: datetime
    track: FullTrack


class SavedTrackPaging(OffsetPaging):
    """Paging of tracks in library."""

    items: List[SavedTrack]
