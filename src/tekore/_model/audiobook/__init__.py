from typing import List, Optional

from ..paging import OffsetPaging
from .base import Audiobook, Author, Narrator


class SimpleAudiobook(Audiobook):
    """
    Simplified audiobook.

    May contain :attr:`chapters`, but that is likely an error.
    """

    chapters: Optional[dict] = None


class SimpleAudiobookPaging(OffsetPaging):
    """Paging of simplified audiobooks."""

    items: List[SimpleAudiobook]
