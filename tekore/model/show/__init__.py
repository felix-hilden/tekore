from typing import List
from dataclasses import dataclass

from tekore.model.show.base import Show
from tekore.model.paging import OffsetPaging
from tekore.serialise import SerialisableDataclass, Timestamp


@dataclass(repr=False)
class SimpleShow(Show):
    pass


@dataclass(repr=False)
class SimpleShowPaging(OffsetPaging):
    items: List[SimpleShow]

    def __post_init__(self):
        self.items = [SimpleShow(**i) for i in self.items]


@dataclass(repr=False)
class SavedShow(SerialisableDataclass):
    added_at: Timestamp
    show: SimpleShow

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.show = SimpleShow(**self.show)


@dataclass(repr=False)
class SavedShowPaging(OffsetPaging):
    items: List[SavedShow]

    def __post_init__(self):
        self.items = [SavedShow(**i) for i in self.items]
