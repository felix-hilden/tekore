from typing import List, Union, Optional
from dataclasses import dataclass

from .base import Item
from .user import PublicUser
from .local import LocalTrack
from .track import FullTrack, Tracks
from .paging import OffsetPaging
from .member import Followers, Image
from .episode import FullEpisode
from .serialise import Model, ModelList, Timestamp

track_type = {
    'track': FullTrack,
    'episode': FullEpisode,
}


@dataclass(repr=False)
class PlaylistTrack(Model):
    """
    Track or episode on a playlist.
    """
    added_at: Timestamp
    added_by: PublicUser
    is_local: bool
    primary_color: str
    video_thumbnail: Optional[Image]
    track: Union[FullTrack, LocalTrack, FullEpisode, None]

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.added_by = PublicUser(**self.added_by)

        if self.video_thumbnail is not None:
            self.video_thumbnail = Image(**self.video_thumbnail)

        if self.track is not None:
            if self.is_local:
                self.track = LocalTrack(**self.track)
            else:
                self.track = track_type[self.track['type']](**self.track)


@dataclass(repr=False)
class PlaylistTrackPaging(OffsetPaging):
    """
    Paging of playlist tracks.
    """
    items: List[PlaylistTrack]

    def __post_init__(self):
        self.items = ModelList(PlaylistTrack(**t) for t in self.items)


@dataclass(repr=False)
class Playlist(Item):
    """
    Playlist base.
    """
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
        self.images = ModelList(Image(**i) for i in self.images)
        self.owner = PublicUser(**self.owner)


@dataclass(repr=False)
class SimplePlaylist(Playlist):
    """
    Simplified playlist object.
    """
    tracks: Tracks

    def __post_init__(self):
        super().__post_init__()
        self.tracks = Tracks(**self.tracks)


@dataclass(repr=False)
class FullPlaylist(Playlist):
    """
    Complete playlist object.
    """
    followers: Followers
    tracks: PlaylistTrackPaging

    def __post_init__(self):
        super().__post_init__()
        self.followers = Followers(**self.followers)
        self.tracks = PlaylistTrackPaging(**self.tracks)


@dataclass(repr=False)
class SimplePlaylistPaging(OffsetPaging):
    """
    Paging of simplified playlists.
    """
    items: List[SimplePlaylist]

    def __post_init__(self):
        self.items = ModelList(SimplePlaylist(**p) for p in self.items)
