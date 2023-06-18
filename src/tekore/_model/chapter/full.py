from ..audiobook import SimpleAudiobook
from .base import Chapter


class FullChapter(Chapter):
    """Complete chapter object."""

    audiobook: SimpleAudiobook
