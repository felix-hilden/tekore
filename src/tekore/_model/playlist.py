from __future__ import annotations

from datetime import datetime
from typing import Literal

from .base import Item
from .episode import FullEpisode
from .local import LocalTrack
from .member import Followers, Image
from .paging import OffsetPaging
from .serialise import Model
from .track import FullTrack, Tracks
from .user import PublicUser


class FullPlaylistTrack(FullTrack):
    """
    Track on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    """

    episode: Literal[False]
    track: Literal[True]
    is_local: Literal[False]


class FullPlaylistEpisode(FullEpisode):
    """
    Episode on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    :attr:`available_markets` is undocumented.
    """

    available_markets: list[str] | None = None
    episode: Literal[True]
    track: Literal[False]


class LocalPlaylistTrack(LocalTrack):
    """
    Local track on a playlist.

    Provides :attr:`episode` and :attr:`track` booleans
    to easily determine the type of playlist item.
    """

    episode: Literal[False] = False
    track: Literal[True] = True


class PlaylistTrack(Model):
    """
    Track or episode on a playlist.

    `track` and `item` are the same, but `track` is deprecated
    and may be removed in a future version.
    """

    added_at: datetime
    added_by: PublicUser
    is_local: bool
    track: FullPlaylistTrack | FullPlaylistEpisode | LocalPlaylistTrack | None = None
    item: FullPlaylistTrack | FullPlaylistEpisode | LocalPlaylistTrack | None = None

    primary_color: str | None
    video_thumbnail: dict | None


class PlaylistTrackPaging(OffsetPaging):
    """Paging of playlist tracks."""

    items: list[PlaylistTrack]


class Playlist(Item):
    """
    Playlist base.

    :attr:`owner` can be ``None`` on featured playlists.
    """

    collaborative: bool
    description: str | None
    external_urls: dict
    images: list[Image] | None
    name: str
    owner: PublicUser
    public: bool | None
    snapshot_id: str

    primary_color: str | None


class SimplePlaylist(Playlist):
    """
    Simplified playlist object.

    `tracks` and `items` are the same, but `tracks` is deprecated
    and may be removed in a future version.
    """

    tracks: Tracks
    items: Tracks


class FullPlaylist(Playlist):
    """
    Complete playlist object.

    `tracks` and `items` are the same, but `tracks` is deprecated
    and may be removed in a future version.
    """

    followers: Followers
    tracks: PlaylistTrackPaging
    items: PlaylistTrackPaging


class SimplePlaylistPaging(OffsetPaging):
    """Paging of simplified playlists."""

    items: list[SimplePlaylist | None]
