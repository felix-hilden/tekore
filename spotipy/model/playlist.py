from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.model.user import PublicUser
from spotipy.model.track import FullTrack, Tracks
from spotipy.model.paging import OffsetPaging
from spotipy.model.member import Followers, Image
from spotipy.serialise import SerialisableDataclass, Timestamp


@dataclass
class PlaylistTrack(SerialisableDataclass):
    added_at: Timestamp
    added_by: PublicUser
    is_local: bool
    track: FullTrack
    primary_color: str
    video_thumbnail: Image

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.added_by = PublicUser(**self.added_by)
        self.track = FullTrack(**self.track)
        self.video_thumbnail = Image(**self.video_thumbnail)


@dataclass
class PlaylistTrackPaging(OffsetPaging):
    items: List[PlaylistTrack]

    def __post_init__(self):
        self.items = [PlaylistTrack(**t) for t in self.items]


@dataclass
class Playlist(Item):
    collaborative: bool
    external_urls: dict
    images: List[Image]
    name: str
    owner: PublicUser
    public: bool
    snapshot_id: str
    primary_color: str

    def __post_init__(self):
        self.images = [Image(**i) for i in self.images]
        self.owner = PublicUser(**self.owner)


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


@dataclass
class SimplePlaylistPaging(OffsetPaging):
    items: List[SimplePlaylist]

    def __post_init__(self):
        self.items = [SimplePlaylist(**p) for p in self.items]
