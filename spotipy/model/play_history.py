from dataclasses import dataclass

from spotipy.model.track import SimpleTrack
from spotipy.model.context import Context


@dataclass
class PlayHistory:
    track: SimpleTrack
    played_at: str
    context: Context

    def __post_init__(self):
        self.track = SimpleTrack(**self.track)
        self.context = Context(**self.context)
