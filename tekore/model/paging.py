from typing import List
from dataclasses import dataclass

from tekore.serialise import SerialisableDataclass


@dataclass(repr=False)
class Paging(SerialisableDataclass):
    href: str
    items: List[SerialisableDataclass]
    limit: int
    next: str


@dataclass(repr=False)
class OffsetPaging(Paging):
    total: int
    offset: int
    previous: str


@dataclass(repr=False)
class Cursor(SerialisableDataclass):
    after: str


@dataclass(repr=False)
class CursorPaging(Paging):
    cursors: Cursor

    def __post_init__(self):
        self.cursors = Cursor(**self.cursors)
