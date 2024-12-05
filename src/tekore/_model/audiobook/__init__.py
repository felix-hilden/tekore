from __future__ import annotations

from tekore._model.paging import OffsetPaging

from .base import Audiobook, Author, Narrator


class SimpleAudiobook(Audiobook):
    """
    Simplified audiobook.

    May contain :attr:`chapters`, but that is likely an error.
    """

    chapters: dict | None = None


class SimpleAudiobookPaging(OffsetPaging):
    """Paging of simplified audiobooks."""

    items: list[SimpleAudiobook]
