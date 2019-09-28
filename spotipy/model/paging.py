from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item
from spotipy.serialise import SerialisableDataclass


@dataclass
class Paging(SerialisableDataclass):
    href: str
    items: List[Item]
    limit: int
    next: str


@dataclass
class OffsetPaging(Paging):
    total: int
    offset: int
    previous: str


@dataclass
class Cursor(SerialisableDataclass):
    after: str


@dataclass
class CursorPaging(Paging):
    cursors: Cursor

    def __post_init__(self):
        self.cursors = Cursor(**self.cursors)
