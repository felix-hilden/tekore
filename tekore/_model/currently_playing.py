from typing import Optional, Union, List
from dataclasses import dataclass

from .context import Context
from .device import Device
from .track import FullTrack
from .local import LocalTrack
from .episode import FullEpisode
from .serialise import Model, StrEnum, ModelList


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
        self.disallows = Disallows.from_kwargs(self.disallows)


item_type = {
    'track': FullTrack,
    'episode': FullEpisode,
}


def _parse_playback_item(item: dict):
    if item.get('is_local', False) is True:
        return LocalTrack.from_kwargs(item)
    else:
        return item_type[item['type']].from_kwargs(item)


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
        self.actions = Actions.from_kwargs(self.actions)
        self.currently_playing_type = CurrentlyPlayingType[
            self.currently_playing_type
        ]

        if self.context is not None:
            self.context = Context.from_kwargs(self.context)
        if self.item is not None:
            self.item = _parse_playback_item(self.item)


@dataclass(repr=False)
class CurrentlyPlayingContext(CurrentlyPlaying):
    """Extended current playback context."""

    device: Device
    repeat_state: RepeatState
    shuffle_state: bool

    def __post_init__(self):
        super().__post_init__()
        self.device = Device.from_kwargs(self.device)
        self.repeat_state = RepeatState[self.repeat_state]


@dataclass(repr=False)
class Queue(Model):
    """Playback queue."""

    currently_playing: Union[FullTrack, LocalTrack, FullEpisode, None]
    queue: List[FullTrack]

    def __post_init__(self):
        self.currently_playing = _parse_playback_item(self.currently_playing)
        self.queue = ModelList(_parse_playback_item(i) for i in self.queue)
