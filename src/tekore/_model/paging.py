from __future__ import annotations

from collections.abc import Sequence

from .serialise import Model


class Paging(Model):
    """Paging base."""

    href: str
    items: Sequence[Model | None]
    limit: int
    next: str | None


class OffsetPaging(Paging):
    """
    Offset paging base.

    Paging that can be navigated both forward and back.
    """

    total: int
    offset: int
    previous: str | None


class Cursor(Model):
    """Data cursor."""

    after: str | None


class CursorPaging(Paging):
    """
    Cursor paging base.

    Paging that can be navigated only forward following the cursor.
    """

    cursors: Cursor
