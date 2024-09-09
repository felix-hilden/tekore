from typing import List, Optional

from ..base import Item
from ..member import Image, ReleaseDatePrecision, Restrictions, ResumePoint


class Chapter(Item):
    """Audiobook chapter base."""

    audio_preview_url: Optional[str]
    available_markets: Optional[List[str]] = None
    chapter_number: int
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    html_description: str
    images: List[Image]
    is_playable: Optional[bool] = None
    languages: List[str]
    name: str
    release_date_precision: ReleaseDatePrecision
    release_date: str
    restrictions: Optional[Restrictions] = None
    resume_point: Optional[ResumePoint] = None
