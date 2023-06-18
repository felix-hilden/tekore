from typing import List

from ..paging import OffsetPaging
from .base import Chapter


class SimpleChapter(Chapter):
    """Simplified chapter."""

    available_markets: List[str] = None


class SimpleChapterPaging(OffsetPaging):
    """Paging of simplified chapters."""

    items: List[SimpleChapter]
