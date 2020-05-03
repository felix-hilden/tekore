from typing import Optional, Union
from dataclasses import dataclass

from tekore.model.context import Context
from tekore.model.device import Device
from tekore.model.track import FullTrack
from tekore.model.episode import FullEpisode
from tekore.model.serialise import Model, StrEnum


class CurrentlyPlayingType(StrEnum):
    ad = 'ad'
    episode = 'episode'
    track = 'track'
    unknown = 'unknown'


class RepeatState(StrEnum):
    off = 'off'
    track = 'track'
    context = 'context'


@dataclass(repr=False)
class Disallows(Model):
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
    Context, progress_ms and item may be None e.g. during a private session.
    """
    actions: Actions
    currently_playing_type: CurrentlyPlayingType
    is_playing: bool
    timestamp: int
    context: Optional[Context]
    progress_ms: Optional[int]
    item: Union[FullTrack, FullEpisode, None]

    def __post_init__(self):
        self.actions = Actions(**self.actions)
        self.currently_playing_type = CurrentlyPlayingType[
            self.currently_playing_type
        ]

        if self.context is not None:
            self.context = Context(**self.context)
        if self.item is not None:
            self.item = item_type[self.item['type']](**self.item)


@dataclass(repr=False)
class CurrentlyPlayingContext(CurrentlyPlaying):
    device: Device
    repeat_state: RepeatState
    shuffle_state: bool

    def __post_init__(self):
        super().__post_init__()
        self.device = Device(**self.device)
        self.repeat_state = RepeatState[self.repeat_state]
