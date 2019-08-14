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


@dataclass
class SimpleTrack(Track):
    pass


@dataclass
class FullTrack(Track):
    album: SimpleAlbum
    external_ids: ExternalID
    popularity: int


@dataclass
class SimpleTrackPaging(OffsetPaging):
    items: List[SimpleTrack]


@dataclass
class Tracks:
    href: str
    total: int


@dataclass
class SavedTrack:
    added_at: str
    track: Track
