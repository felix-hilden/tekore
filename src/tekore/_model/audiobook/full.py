from ..chapter import SimpleChapterPaging
from .base import Audiobook


class FullAudiobook(Audiobook):
    """Complete audiobook object."""

    chapters: SimpleChapterPaging
