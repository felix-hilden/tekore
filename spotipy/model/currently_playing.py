from dataclasses import dataclass

from spotipy.serialise import SerialisableEnum, SerialisableDataclass
from spotipy.model.context import Context
from spotipy.model.track import FullTrack

CurrentlyPlayingType = SerialisableEnum(
    'CurrentlyPlayingType',
    'track episode ad unknown'
)


@dataclass
class CurrentlyPlaying(SerialisableDataclass):
    timestamp: int
    is_playing: bool
    currently_playing_type: CurrentlyPlayingType
    context: Context = None
    progress_ms: int = None
    item: FullTrack = None

    def __post_init__(self):
        self.currently_playing_type = CurrentlyPlayingType[
            self.currently_playing_type
        ]
