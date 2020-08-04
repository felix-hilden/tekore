from typing import Optional, Union
from dataclasses import dataclass

from .context import Context
from .device import Device
from .track import FullTrack
from .local import LocalTrack
from .episode import FullEpisode
from .serialise import Model, StrEnum


class CurrentlyPlayingType(StrEnum):
    """Type of currently playing item."""

    ad = 'ad'
    episode = 'episode'
    track = 'track'
    unknown = 'unknown'


class RepeatState(StrEnum):
    """Playback repeat state."""

    off = 'off'
    track = 'track'
    context = 'context'


@dataclass(repr=False)
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


@dataclass(repr=False)
class Actions(Model):
    """Player actions."""

    disallows: Disallows

    def __post_init__(self):
        self.disallows = Disallows(**self.disallows)


item_type = {
    'track': FullTrack,
    'episode': FullEpisode,
}


@dataclass(repr=False)
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
    context: Optional[Context]
    progress_ms: Optional[int]
    item: Union[FullTrack, LocalTrack, FullEpisode, None]

    def __post_init__(self):
        self.actions = Actions(**self.actions)
        self.currently_playing_type = CurrentlyPlayingType[
            self.currently_playing_type
        ]

        if self.context is not None:
            self.context = Context(**self.context)
        if self.item is not None:
            if self.item.get('is_local', False) is True:
                self.item = LocalTrack(**self.item)
            else:
                self.item = item_type[self.item['type']](**self.item)


@dataclass(repr=False)
class CurrentlyPlayingContext(CurrentlyPlaying):
    """Extended current playback context."""

    device: Device
    repeat_state: RepeatState
    shuffle_state: bool

    def __post_init__(self):
        super().__post_init__()
        self.device = Device(**self.device)
        self.repeat_state = RepeatState[self.repeat_state]
