from enum import Enum
from dataclasses import dataclass

from spotipy.serialise import SerialisableDataclass, SerialisableEnum
from spotipy.model.context import Context
from spotipy.model.device import Device
from spotipy.model.track import FullTrack

CurrentlyPlayingType = Enum('CurrentlyPlayingType', 'track episode ad unknown')
RepeatState = SerialisableEnum('RepeatState', 'off track context')


@dataclass
class Disallows(SerialisableDataclass):
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


@dataclass
class Actions(SerialisableDataclass):
    disallows: Disallows

    def __post_init__(self):
        self.disallows = Disallows(**self.disallows)


@dataclass
class CurrentlyPlaying(SerialisableDataclass):
    actions: Actions
    currently_playing_type: CurrentlyPlayingType
    is_playing: bool
    timestamp: int

    def __post_init__(self):
        self.actions = Actions(**self.actions)
        self.currently_playing_type = CurrentlyPlayingType[
            self.currently_playing_type
        ]


@dataclass
class CurrentlyPlayingContext(CurrentlyPlaying):
    device: Device
    repeat_state: RepeatState
    shuffle_state: bool
    context: Context = None
    progress_ms: int = None
    item: FullTrack = None

    def __post_init__(self):
        super().__post_init__()
        self.device = Device(**self.device)
        self.repeat_state = RepeatState[self.repeat_state]

        if self.context is not None:
            self.context = Context(**self.context)
        if self.item is not None:
            self.item = FullTrack(**self.item)


@dataclass
class CurrentlyPlayingTrack(CurrentlyPlaying):
    context: Context = None
    progress_ms: int = None
    item: FullTrack = None

    def __post_init__(self):
        super().__post_init__()
        if self.context is not None:
            self.context = Context(**self.context)
        if self.item is not None:
            self.item = FullTrack(**self.item)
