from typing import List, Optional
from dataclasses import dataclass

from ..paging import OffsetPaging
from ..serialise import ModelList
from .base import Audiobook, Author, Narrator


@dataclass(repr=False)
class SimpleAudiobook(Audiobook):
    """Simplified audiobook."""

    available_markets: Optional[List[str]] = None


@dataclass(repr=False)
class SimpleAudiobookPaging(OffsetPaging):
    """Paging of simplified audiobooks."""

    items = List[SimpleAudiobook]

    def __post_init__(self):
        self.items = ModelList(SimpleAudiobook.from_kwargs(i) for i in self.items)
