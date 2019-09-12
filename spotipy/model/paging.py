from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.serialise import SerialisableDataclass


@dataclass
class Paging(SerialisableDataclass):
    href: str
    items: List[Item]
    limit: int
    total: int
    next: str

    def __post_init__(self):
        self.items = [Item(**i) for i in self.items]


@dataclass
class OffsetPaging(Paging):
    offset: int
    previous: str


@dataclass
class Cursor(SerialisableDataclass):
    after: str


@dataclass
class CursorPaging(Paging):
    cursors: Cursor

    def __post_init__(self):
        super().__post_init__()
        self.cursors = Cursor(**self.cursors)
