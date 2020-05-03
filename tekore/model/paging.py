from typing import List
from dataclasses import dataclass

from tekore.model.serialise import Model


@dataclass(repr=False)
class Paging(Model):
    href: str
    items: List[Model]
    limit: int
    next: str


@dataclass(repr=False)
class OffsetPaging(Paging):
    total: int
    offset: int
    previous: str


@dataclass(repr=False)
class Cursor(Model):
    after: str


@dataclass(repr=False)
class CursorPaging(Paging):
    cursors: Cursor

    def __post_init__(self):
        self.cursors = Cursor(**self.cursors)
