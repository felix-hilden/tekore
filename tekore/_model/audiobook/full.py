from typing import List, Optional
from dataclasses import dataclass

from ..chapter import SimpleChapterPaging
from .base import Audiobook


@dataclass(repr=False)
class FullAudiobook(Audiobook):
    """Complete audiobook object."""

    chapters: SimpleChapterPaging
    available_markets: Optional[List[str]] = None

    def __post_init__(self):
        super().__post_init__()
        self.chapters = SimpleChapterPaging.from_kwargs(self.chapters)
