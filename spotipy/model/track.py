from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.album import SimpleAlbum
from spotipy.model.artist import SimpleArtist
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import Restrictions, Timestamp
from spotipy.serialise import SerialisableDataclass


@dataclass
class TrackLink(Item):
    external_urls: dict


@dataclass
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
        self.artists = [SimpleArtist(**a) for a in self.artists]


@dataclass
class SimpleTrack(Track):
    available_markets: List[str] = None
    linked_from: TrackLink = None
    is_playable: bool = None
    restrictions: Restrictions = None

    def __post_init__(self):
        super().__post_init__()
        if self.linked_from is not None:
            self.linked_from = TrackLink(**self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass
class FullTrack(Track):
    album: SimpleAlbum
    external_ids: dict
    popularity: int
    available_markets: List[str] = None
    linked_from: TrackLink = None
    is_playable: bool = None
    restrictions: Restrictions = None

    def __post_init__(self):
        super().__post_init__()
        self.album = SimpleAlbum(**self.album)
        if self.linked_from is not None:
            self.linked_from = TrackLink(**self.linked_from)
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass
class FullTrackPaging(OffsetPaging):
    items: List[SimpleTrack]

    def __post_init__(self):
        self.items = [FullTrack(**t) for t in self.items]


@dataclass
class SimpleTrackPaging(OffsetPaging):
    items: List[SimpleTrack]

    def __post_init__(self):
        self.items = [SimpleTrack(**t) for t in self.items]


@dataclass
class Tracks(SerialisableDataclass):
    href: str
    total: int


@dataclass
class SavedTrack(SerialisableDataclass):
    added_at: Timestamp
    track: Track

    def __post_init__(self):
        self.added_at = Timestamp(datetime=self.added_at)
        self.track = Track(**self.track)


@dataclass
class SavedTrackPaging(OffsetPaging):
    items: List[SavedTrack]

    def __post_init__(self):
        self.items = [SavedTrack(**t) for t in self.items]
