from __future__ import annotations

from typing import Union

from .context import Context
from .device import Device
from .episode import FullEpisode
from .local import LocalTrack
from .serialise import Model, StrEnum
from .track import FullTrack


class CurrentlyPlayingType(StrEnum):
    """Type of currently playing item."""

    ad = "ad"
    episode = "episode"
    track = "track"
    unknown = "unknown"


class RepeatState(StrEnum):
    """Playback repeat state."""

    off = "off"
    track = "track"
    context = "context"


class Disallows(Model):
    """Disallowed player actions."""

    interrupting_playback: bool = False
    pausing: bool = False
    resuming: bool = False
    seeking: bool = False
    skipping_next: bool = False
    skipping_prev: bool = False
    toggling_repeat_context: bool = False
    toggling_shuffle: bool = False
    toggling_repeat_track: bool = False
    transferring_playback: bool = False


class Actions(Model):
    """Player actions."""

    disallows: Disallows


PlaybackItem = Union[FullTrack, LocalTrack, FullEpisode, None]


class CurrentlyPlaying(Model):
    """
    Current playback.

    :attr:`context`, :attr:`progress_ms` and :attr:`item` may be ``None``
    e.g. during a private session.
    """

    actions: Actions
    currently_playing_type: CurrentlyPlayingType
    is_playing: bool
    timestamp: int
    context: Context | None
    progress_ms: int | None
    item: PlaybackItem


class CurrentlyPlayingContext(CurrentlyPlaying):
    """
    Extended current playback context.

    ``smart_shuffle`` is not documented in the Spotify API.
    """

    device: Device
    repeat_state: RepeatState
    shuffle_state: bool
    smart_shuffle: bool | None


class Queue(Model):
    """Playback queue."""

    currently_playing: PlaybackItem
    queue: list[PlaybackItem]
