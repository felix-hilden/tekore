from typing import List
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.album import SimpleAlbum
from tekore.model.artist import SimpleArtist
from tekore.model.paging import OffsetPaging
from tekore.model.member import Restrictions
from tekore.model.serialise import Model, ModelList, Timestamp


@dataclass(repr=False)
class TrackLink(Item):
    external_urls: dict


@dataclass(repr=False)
class Track(Item):
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
        self.artists = ModelList(SimpleArtist(**a) for a in self.artists)


@dataclass(repr=False)
class SimpleTrack(Track):
    """
    Available markets are not available when market is specified.
    Is playable is not available when market is None.
    Restrictions is available if restrictions have been placed on
    the track, making it unplayable.
    """
    available_markets: List[str] = None
    linked_from: TrackLink = None
    is_playable: bool = None
    restrictions: Restrictions = None

    def __post_init__(self):
        super().__post_init__()
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)
        if self.linked_from is not None:
            self.linked_from = TrackLink(**self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass(repr=False)
class FullTrack(Track):
    """
    Available markets are not available when market is specified.
    Is playable is not available when market is None.
    Restrictions is available if restrictions have been placed on
    the track, making it unplayable.

    Episode and track are only available on a playlist.
    """
    album: SimpleAlbum
    external_ids: dict
    popularity: int
    available_markets: List[str] = None
    linked_from: TrackLink = None
    is_playable: bool = None
    restrictions: Restrictions = None
    episode: bool = None
    track: bool = None

    def __post_init__(self):
        super().__post_init__()
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)
        self.album = SimpleAlbum(**self.album)
        if self.linked_from is not None:
            self.linked_from = TrackLink(**self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass(repr=False)
class FullTrackPaging(OffsetPaging):
    items: List[FullTrack]

    def __post_init__(self):
        self.items = ModelList(FullTrack(**t) for t in self.items)


@dataclass(repr=False)
class SimpleTrackPaging(OffsetPaging):
    items: List[SimpleTrack]

    def __post_init__(self):
        self.items = ModelList(SimpleTrack(**t) for t in self.items)


@dataclass(repr=False)
class Tracks(Model):
    href: str
    total: int


@dataclass(repr=False)
class SavedTrack(Model):
    added_at: Timestamp
    track: FullTrack

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.track = FullTrack(**self.track)


@dataclass(repr=False)
class SavedTrackPaging(OffsetPaging):
    items: List[SavedTrack]

    def __post_init__(self):
        self.items = ModelList(SavedTrack(**t) for t in self.items)
