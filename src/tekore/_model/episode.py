from __future__ import annotations

from datetime import datetime

from .base import Item
from .member import Image, ReleaseDatePrecision, Restrictions, ResumePoint
from .paging import OffsetPaging
from .serialise import Model
from .show import SimpleShow


class Episode(Item):
    """
    Episode base.

    :attr:`language` is deprecated.
    """

    audio_preview_url: str | None
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    html_description: str
    images: list[Image]
    is_externally_hosted: bool
    is_playable: bool | None = None
    language: str | None = None
    languages: list[str]
    name: str
    release_date: str
    release_date_precision: ReleaseDatePrecision
    resume_point: ResumePoint | None = None


class SimpleEpisode(Episode):
    """Simplified episode object."""


class FullEpisode(Episode):
    """Complete episode object."""

    restrictions: Restrictions | None = None
    show: SimpleShow


class SimpleEpisodePaging(OffsetPaging):
    """Paging of simplified episodes."""

    items: list[SimpleEpisode]


class SavedEpisode(Model):
    """Episode saved to library."""

    added_at: datetime
    episode: FullEpisode


class SavedEpisodePaging(OffsetPaging):
    """Paging of episodes in library."""

    items: list[SavedEpisode]
