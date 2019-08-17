from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.user import User
from spotipy.model.track import Track, Tracks
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import Followers, Image


@dataclass
class PlaylistTrack:
    added_at: str
    added_by: User
    is_local: bool
    track: Track

    def __post_init__(self):
        self.added_by = User(**self.added_by)
        self.track = Track(**self.track)


@dataclass
class PlaylistTrackPaging(OffsetPaging):
    pass


@dataclass
class Playlist(Item):
    collaborative: bool
    external_urls: dict
    images: List[Image]
    name: str
    owner: User
    public: bool
    snapshot_id: str

    def __post_init__(self):
        self.images = [Image(**i) for i in self.images]
        self.owner = User(**self.owner)


@dataclass
class SimplePlaylist(Playlist):
    tracks: Tracks

    def __post_init__(self):
        super().__post_init__()
        self.tracks = Tracks(**self.tracks)


@dataclass
class FullPlaylist(Playlist):
    description: str
    followers: Followers
    tracks: PlaylistTrackPaging

    def __post_init__(self):
        super().__post_init__()
        self.followers = Followers(**self.followers)
        self.tracks = PlaylistTrackPaging(**self.tracks)
