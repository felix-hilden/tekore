from typing import List, Optional
from dataclasses import dataclass

from ..paging import OffsetPaging
from ..serialise import ModelList
from ..member import Restrictions
from .base import Chapter


@dataclass(repr=False)
class SimpleChapter(Chapter):
    """Simplified chapter."""

    available_markets: List[str] = None
    restriction: Optional[Restrictions] = None

    def __post_init__(self):
        super().__post_init__()
        if self.restriction:
            self.restriction = Restrictions(**self.restriction)


@dataclass(repr=False)
class SimpleChapterPaging(OffsetPaging):
    """Paging of simplified chapters."""

    items = List[SimpleChapter]

    def __post_init__(self):
        self.items = ModelList(SimpleChapter(**i) for i in self.items)
