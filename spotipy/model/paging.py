from typing import List, Optional
from dataclasses import dataclass

from spotipy.model.base import Item


@dataclass
class Paging:
    href: str
    items: List[Item]
    limit: int
    next: Optional[str]
    total: int


@dataclass
class OffsetPaging(Paging):
    offset: int
    previous: Optional[str]


@dataclass
class Cursor:
    after: str


@dataclass
class CursorPaging(Paging):
    cursors: Cursor
