from datetime import datetime
from typing import List
from dataclasses import dataclass

from spotipy.model.track import FullTrack
from spotipy.model.context import Context
from spotipy.model.paging import CursorPaging, Cursor
from spotipy.serialise import SerialisableDataclass


@dataclass
class MillisecondTimestamp:
    datetime: datetime

    def __post_init__(self):
        self.datetime = datetime.strptime(
            self.datetime, '%Y-%m-%dT%H:%M:%S.%f%z'
        )

    def __str__(self):
        return self.datetime.isoformat(timespec='milliseconds') + 'Z'


@dataclass
class PlayHistory(SerialisableDataclass):
    track: FullTrack
    played_at: MillisecondTimestamp
    context: Context = None

    def __post_init__(self):
        self.track = FullTrack(**self.track)
        self.played_at = MillisecondTimestamp(datetime=self.played_at)

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
