from typing import Optional, Sequence

from .serialise import Model


class Paging(Model):
    """Paging base."""

    href: str
    items: Sequence[Model]
    limit: int
    next: Optional[str]


class OffsetPaging(Paging):
    """
    Offset paging base.

    Paging that can be navigated both forward and back.
    """

    total: int
    offset: int
    previous: Optional[str]


class Cursor(Model):
    """Data cursor."""

    after: Optional[str]


class CursorPaging(Paging):
    """
    Cursor paging base.

    Paging that can be navigated only forward following the cursor.
    """

    cursors: Cursor
