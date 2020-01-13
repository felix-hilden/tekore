from typing import List, Union
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.user import PublicUser
from tekore.model.local import LocalTrack
from tekore.model.track import FullTrack, Tracks
from tekore.model.paging import OffsetPaging
from tekore.model.member import Followers, Image
from tekore.serialise import SerialisableDataclass, Timestamp


@dataclass
class PlaylistTrack(SerialisableDataclass):
    added_at: Timestamp
    added_by: PublicUser
    is_local: bool
    primary_color: str
    video_thumbnail: Image
    track: Union[FullTrack, LocalTrack, None]

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.added_by = PublicUser(**self.added_by)
        self.video_thumbnail = Image(**self.video_thumbnail)

        if self.track is not None:
            if self.is_local:
                self.track = LocalTrack(**self.track)
            else:
                self.track = FullTrack(**self.track)


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
    description: str

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
