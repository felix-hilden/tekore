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


@dataclass(repr=False)
class FullPlaylistTrack(FullTrack):
    """
    Track on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    """

    episode: bool = False
    track: bool = True


@dataclass(repr=False)
class FullPlaylistEpisode(FullEpisode):
    """
    Episode on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    """

    episode: bool = True
    track: bool = False


@dataclass(repr=False)
class LocalPlaylistTrack(LocalTrack):
    """
    Local track on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    """

    episode: bool = False
    track: bool = True


track_type = {
    'track': FullPlaylistTrack,
    'episode': FullPlaylistEpisode,
}


@dataclass(repr=False)
class PlaylistTrack(Model):
    """Track or episode on a playlist."""

    added_at: Timestamp
    added_by: PublicUser
    is_local: bool
    primary_color: str
    video_thumbnail: Optional[Image]
    track: Union[FullPlaylistTrack, LocalPlaylistTrack, FullPlaylistEpisode, None]

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.added_by = PublicUser(**self.added_by)

        if self.video_thumbnail is not None:
            self.video_thumbnail = Image(**self.video_thumbnail)

        if self.track is not None:
            if self.is_local:
                self.track = LocalPlaylistTrack(**self.track)
            else:
                self.track = track_type[self.track['type']](**self.track)


@dataclass(repr=False)
class PlaylistTrackPaging(OffsetPaging):
    """Paging of playlist tracks."""

    items: List[PlaylistTrack]

    def __post_init__(self):
        self.items = ModelList(PlaylistTrack(**t) for t in self.items)


@dataclass(repr=False)
class Playlist(Item):
    """
    Playlist base.

    :attr:`owner` can be ``None`` on featured playlists.
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
        if self.owner is not None:
            self.owner = PublicUser(**self.owner)


@dataclass(repr=False)
class SimplePlaylist(Playlist):
    """Simplified playlist object."""

    tracks: Tracks

    def __post_init__(self):
        super().__post_init__()
        self.tracks = Tracks(**self.tracks)


@dataclass(repr=False)
class FullPlaylist(Playlist):
    """Complete playlist object."""

    followers: Followers
    tracks: PlaylistTrackPaging

    def __post_init__(self):
        super().__post_init__()
        self.followers = Followers(**self.followers)
        self.tracks = PlaylistTrackPaging(**self.tracks)


@dataclass(repr=False)
class SimplePlaylistPaging(OffsetPaging):
    """Paging of simplified playlists."""

    items: List[SimplePlaylist]

    def __post_init__(self):
        self.items = ModelList(SimplePlaylist(**p) for p in self.items)
