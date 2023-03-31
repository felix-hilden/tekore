from dataclasses import dataclass
from typing import Optional

from ..audiobook.full import FullAudiobook
from ..member import Restrictions
from .base import Chapter


@dataclass(repr=False)
class FullChapter(Chapter):
    """Complete chapter object."""

    audiobook: FullAudiobook
    is_playable: Optional[bool] = None
    restrictions: Optional[Restrictions] = None

    def __post_init__(self):
        super().__post_init__()
        self.audiobook = FullAudiobook.from_kwargs(self.audiobook)
        if self.restrictions:
            self.restrictions = Restrictions.from_kwargs(self.restrictions)
