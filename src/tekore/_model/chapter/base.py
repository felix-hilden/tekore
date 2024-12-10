from __future__ import annotations

from tekore._model.base import Item
from tekore._model.member import Image, ReleaseDatePrecision, Restrictions, ResumePoint


class Chapter(Item):
    """Audiobook chapter base."""

    audio_preview_url: str | None
    available_markets: list[str] | None = None
    chapter_number: int
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    html_description: str
    images: list[Image]
    is_playable: bool | None = None
    languages: list[str]
    name: str
    release_date_precision: ReleaseDatePrecision
    release_date: str
    restrictions: Restrictions | None = None
    resume_point: ResumePoint | None = None
