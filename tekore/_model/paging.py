from typing import Sequence
from dataclasses import dataclass

from .serialise import Model


@dataclass(repr=False)
class Paging(Model):
    """Paging base."""

    href: str
    items: Sequence[Model]
    limit: int
    next: str


@dataclass(repr=False)
class OffsetPaging(Paging):
    """
    Offset paging base.

    Paging that can be navigated both forward and back.
    """

    total: int
    offset: int
    previous: str


@dataclass(repr=False)
class Cursor(Model):
    """Data cursor."""

    after: str


@dataclass(repr=False)
class CursorPaging(Paging):
    """
    Cursor paging base.

    Paging that can be navigated only forward following the cursor.
    """

    cursors: Cursor

    def __post_init__(self):
        self.cursors = Cursor(**self.cursors)
