from typing import List

from ..paging import OffsetPaging
from .base import Chapter


class SimpleChapter(Chapter):
    """Simplified chapter."""


class SimpleChapterPaging(OffsetPaging):
    """Paging of simplified chapters."""

    items: List[SimpleChapter]
