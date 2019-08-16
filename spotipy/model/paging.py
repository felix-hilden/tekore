from typing import List
from dataclasses import dataclass

from spotipy.model.base import Item


@dataclass
class Paging:
    href: str
    items: List[Item]
    limit: int
    total: int


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
