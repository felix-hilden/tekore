from typing import Optional

from ..chapter import SimpleChapterPaging
from .base import Audiobook


class FullAudiobook(Audiobook):
    """Complete audiobook object."""

    chapters: SimpleChapterPaging
    is_playable: Optional[bool] = None
