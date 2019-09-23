from typing import List
from dataclasses import dataclass

from spotipy.model.track import SimpleTrack
from spotipy.model.member import Timestamp
from spotipy.model.context import Context
from spotipy.model.paging import CursorPaging
from spotipy.serialise import SerialisableDataclass


@dataclass
class PlayHistory(SerialisableDataclass):
    track: SimpleTrack
    played_at: Timestamp
    context: Context

    def __post_init__(self):
        self.track = SimpleTrack(**self.track)
        self.played_at = Timestamp(datetime=self.played_at)
        self.context = Context(**self.context)


@dataclass
class PlayHistoryPaging(CursorPaging):
    items: List[PlayHistory]

    def __post_init__(self):
        self.items = [PlayHistory(**h) for h in self.items]
