from typing import List
from dataclasses import dataclass

from spotipy.model.track import FullTrack
from spotipy.model.context import Context
from spotipy.model.paging import CursorPaging, Cursor
from spotipy.serialise import SerialisableDataclass, Timestamp


@dataclass
class PlayHistory(SerialisableDataclass):
    track: FullTrack
    played_at: Timestamp
    context: Context = None

    def __post_init__(self):
        self.track = FullTrack(**self.track)
        self.played_at = Timestamp.from_string(self.played_at)

        if self.context is not None:
            self.context = Context(**self.context)


@dataclass
class PlayHistoryCursor(Cursor):
    before: str


@dataclass
class PlayHistoryPaging(CursorPaging):
    items: List[PlayHistory]

    def __post_init__(self):
        self.cursors = PlayHistoryCursor(**self.cursors)
        self.items = [PlayHistory(**h) for h in self.items]
