from dataclasses import dataclass
from typing import List

from ..paging import OffsetPaging
from ..serialise import Model, ModelList, Timestamp
from ..show.base import Show


@dataclass(repr=False)
class SimpleShow(Show):
    """
    Simplified show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """


@dataclass(repr=False)
class SimpleShowPaging(OffsetPaging):
    """Paging of simplified shows."""

    items: List[SimpleShow]

    def __post_init__(self):
        self.items = ModelList(SimpleShow.from_kwargs(i) for i in self.items)


@dataclass(repr=False)
class SavedShow(Model):
    """Show saved in library."""

    added_at: Timestamp
    show: SimpleShow

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.show = SimpleShow.from_kwargs(self.show)


@dataclass(repr=False)
class SavedShowPaging(OffsetPaging):
    """Paging of shows in library."""

    items: List[SavedShow]

    def __post_init__(self):
        self.items = ModelList(SavedShow.from_kwargs(i) for i in self.items)
