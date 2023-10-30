from datetime import datetime
from typing import List, Optional

from .base import Item
from .member import Image, ReleaseDatePrecision, ResumePoint
from .paging import OffsetPaging
from .serialise import Model
from .show import SimpleShow


class Episode(Item):
    """Episode base."""

    audio_preview_url: Optional[str]
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    html_description: str
    images: List[Image]
    is_externally_hosted: bool
    is_playable: bool
    language: str
    languages: List[str]
    name: str
    release_date: str
    release_date_precision: ReleaseDatePrecision


class SimpleEpisode(Episode):
    """Simplified episode object."""

    resume_point: Optional[ResumePoint] = None


class FullEpisode(Episode):
    """Complete episode object."""

    show: SimpleShow
    resume_point: Optional[ResumePoint] = None


class SimpleEpisodePaging(OffsetPaging):
    """Paging of simplified episodes."""

    items: List[SimpleEpisode]


class SavedEpisode(Model):
    """Episode saved to library."""

    added_at: datetime
    episode: FullEpisode


class SavedEpisodePaging(OffsetPaging):
    """Paging of episodes in library."""

    items: List[SavedEpisode]
