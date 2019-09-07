from dataclasses import dataclass

from spotipy.enumerate import SerialisableEnum
from spotipy.model.context import Context
from spotipy.model.track import FullTrack

CurrentlyPlayingType = SerialisableEnum(
    'CurrentlyPlayingType',
    'track episode ad unknown'
)


@dataclass
class CurrentlyPlaying:
    timestamp: int
    is_playing: bool
    currently_playing_type: str
    context: Context = None
    progress_ms: int = None
    item: FullTrack = None
