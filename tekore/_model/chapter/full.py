from typing import Optional
from dataclasses import dataclass

from .base import Chapter
from ..member import Restrictions
from ..audiobook.full import FullAudiobook


@dataclass(repr=False)
class FullChapter(Chapter):
    """Complete chapter object."""

    audiobook: FullAudiobook
    is_playable: Optional[bool] = None
    restriction: Optional[Restrictions] = None

    def __post_init__(self):
        super().__post_init__()
        self.audiobook = FullAudiobook.from_kwargs(self.audiobook)
        if self.restriction:
            self.restriction = Restrictions.from_kwargs(self.restriction)
