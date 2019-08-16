from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.album import SimpleAlbum
from spotipy.model.artist import SimpleArtist
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import ExternalID, ExternalURL, Restrictions


@dataclass
class TrackLink(Item):
    external_urls: ExternalURL

    def __post_init__(self):
        self.external_urls = ExternalURL(**self.external_urls)


@dataclass
class Track(Item):
    artists: List[SimpleArtist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalURL
    is_playable: bool
    linked_from: TrackLink
    restrictions: Restrictions
    name: str
    preview_url: str
    track_number: int
    is_local: bool

    def __post_init__(self):
        self.artists = [SimpleArtist(**a) for a in self.artists]
        self.external_urls = ExternalURL(**self.external_urls)
        self.linked_from = TrackLink(**self.linked_from)
        self.restrictions = Restrictions(**self.restrictions)


@dataclass
class SimpleTrack(Track):
    pass


@dataclass
class FullTrack(Track):
    album: SimpleAlbum
    external_ids: ExternalID
    popularity: int

    def __post_init__(self):
        super().__post_init__()
        self.album = SimpleAlbum(**self.album)
        self.external_ids = ExternalID(**self.external_ids)


@dataclass
class SimpleTrackPaging(OffsetPaging):
    items: List[SimpleTrack]

    def __post_init__(self):
        self.items = [SimpleTrack(**t) for t in self.items]


@dataclass
class Tracks:
    href: str
    total: int


@dataclass
class SavedTrack:
    added_at: str
    track: Track

    def __post_init__(self):
        self.track = Track(**self.track)
