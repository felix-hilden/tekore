from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item


@dataclass
class Paging:
    href: str
    items: List[Item]
    limit: int
    total: int
    next: str = None

    def __post_init__(self):
        self.items = [Item(**i) for i in self.items]


@dataclass
class OffsetPaging(Paging):
    offset: int
    previous: str = None


@dataclass
class Cursor:
    after: str


@dataclass
class CursorPaging(Paging):
    cursors: Cursor

    def __post_init__(self):
        super().__post_init__()
        self.cursors = Cursor(**self.cursors)
