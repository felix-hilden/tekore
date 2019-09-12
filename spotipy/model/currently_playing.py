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
    currently_playing_type: str
    context: Context = None
    progress_ms: int = None
    item: FullTrack = None
