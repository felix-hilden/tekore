from typing import List, Optional
from dataclasses import dataclass

from .track import FullTrack
from .paging import CursorPaging, Cursor
from .context import Context
from .serialise import Model, ModelList, Timestamp


@dataclass(repr=False)
class PlayHistory(Model):
    """
    Previously played track.

    Context is supposedly sometimes available.
    """

    track: FullTrack
    played_at: Timestamp
    context: Optional[Context]

    def __post_init__(self):
        self.track = FullTrack(**self.track)
        self.played_at = Timestamp.from_string(self.played_at)

        if self.context is not None:
            self.context = Context(**self.context)


@dataclass(repr=False)
class PlayHistoryCursor(Cursor):
    """Cursor to play history."""

    before: str


@dataclass(repr=False)
class PlayHistoryPaging(CursorPaging):
    """
    Paging to play history.

    Cursors are not available when paging is exhausted.
    """

    items: List[PlayHistory]
    cursors: PlayHistoryCursor

    def __post_init__(self):
        if self.cursors is not None:
            self.cursors = PlayHistoryCursor(**self.cursors)
        self.items = ModelList(PlayHistory(**h) for h in self.items)
