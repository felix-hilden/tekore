from dataclasses import dataclass

from spotipy.model.track import SimpleTrack
from spotipy.model.context import Context


@dataclass
class PlayHistory:
    track: SimpleTrack
    played_at: str
    context: Context
