from typing import List, Optional
from dataclasses import dataclass

from .base import Item
from .album import SimpleAlbum
from .artist import SimpleArtist
from .member import Restrictions
from .paging import OffsetPaging
from .serialise import Model, ModelList, Timestamp


@dataclass(repr=False)
class TrackLink(Item):
    """Relinked track."""

    external_urls: dict


@dataclass(repr=False)
class Track(Item):
    """Track base."""

    artists: List[SimpleArtist]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: dict
    name: str
    preview_url: str
    track_number: int
    is_local: bool

    def __post_init__(self):
        self.artists = ModelList(SimpleArtist.from_kwargs(a) for a in self.artists)


@dataclass(repr=False)
class SimpleTrack(Track):
    """
    Simplified track object.

    When market is specified, :attr:`available_markets` is not available.
    :attr:`is_playable` is not available when market is not specified.
    :attr:`restrictions` is available if restrictions have been placed on
    the track, making it unplayable.
    """

    available_markets: Optional[List[str]] = None
    linked_from: Optional[TrackLink] = None
    is_playable: Optional[bool] = None
    restrictions: Optional[Restrictions] = None

    def __post_init__(self):
        super().__post_init__()
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)
        if self.linked_from is not None:
            self.linked_from = TrackLink.from_kwargs(self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions.from_kwargs(self.restrictions)


@dataclass(repr=False)
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
    available_markets: Optional[List[str]] = None
    linked_from: Optional[TrackLink] = None
    is_playable: Optional[bool] = None
    restrictions: Optional[Restrictions] = None

    def __post_init__(self):
        super().__post_init__()
        self.album = SimpleAlbum.from_kwargs(self.album)
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)
        if self.linked_from is not None:
            self.linked_from = TrackLink.from_kwargs(self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions.from_kwargs(self.restrictions)


@dataclass(repr=False)
class FullTrackPaging(OffsetPaging):
    """Paging of full tracks."""

    items: List[FullTrack]

    def __post_init__(self):
        self.items = ModelList(FullTrack.from_kwargs(t) for t in self.items)


@dataclass(repr=False)
class SimpleTrackPaging(OffsetPaging):
    """Paging of simplified tracks."""

    items: List[SimpleTrack]

    def __post_init__(self):
        self.items = ModelList(SimpleTrack.from_kwargs(t) for t in self.items)


@dataclass(repr=False)
class Tracks(Model):
    """Minimal representation of playlist tracks."""

    href: str
    total: int


@dataclass(repr=False)
class SavedTrack(Model):
    """Track saved to library."""

    added_at: Timestamp
    track: FullTrack

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.track = FullTrack.from_kwargs(self.track)


@dataclass(repr=False)
class SavedTrackPaging(OffsetPaging):
    """Paging of tracks in library."""

    items: List[SavedTrack]

    def __post_init__(self):
        self.items = ModelList(SavedTrack.from_kwargs(t) for t in self.items)
