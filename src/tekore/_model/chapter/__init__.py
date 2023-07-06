from typing import List, Optional

from ..paging import OffsetPaging
from .base import Chapter


class SimpleChapter(Chapter):
    """Simplified chapter."""

    available_markets: Optional[List[str]] = None


class SimpleChapterPaging(OffsetPaging):
    """Paging of simplified chapters."""

    items: List[SimpleChapter]
