from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.user import User
from spotipy.model.track import Track, Tracks
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import ExternalURL, Followers, Image


@dataclass
class PlaylistTrack:
    added_at: str
    added_by: User
    is_local: bool
    track: Track


@dataclass
class PlaylistTrackPaging(OffsetPaging):
    pass


@dataclass
class Playlist(Item):
    collaborative: bool
    external_urls: ExternalURL
    images: List[Image]
    name: str
    owner: User
    public: bool
    snapshot_id: str


@dataclass
class SimplePlaylist(Playlist):
    tracks: Tracks


@dataclass
class FullPlaylist(Playlist):
    description: str
    followers: Followers
    tracks: PlaylistTrackPaging
