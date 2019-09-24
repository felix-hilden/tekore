from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.user import User
from spotipy.model.track import Track, Tracks
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import Followers, Image, Timestamp
from spotipy.serialise import SerialisableDataclass


@dataclass
class PlaylistTrack(SerialisableDataclass):
    added_at: Timestamp
    added_by: User
    is_local: bool
    track: Track

    def __post_init__(self):
        self.added_at = Timestamp(datetime=self.added_at)
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
    primary_color: str

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


@dataclass
class SimplePlaylistPaging(OffsetPaging):
    items: List[SimplePlaylist]

    def __post_init__(self):
        self.items = [SimplePlaylist(**p) for p in self.items]
