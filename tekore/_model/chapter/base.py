from typing import List, Optional
from dataclasses import dataclass

from ..base import Item
from ..member import Image, ReleaseDatePrecision, ResumePoint
from ..serialise import ModelList


@dataclass(repr=False)
class Chapter(Item):
    """Audiobook chapter base."""

    audio_preview_url: Optional[str]
    chapter_number: int
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    html_description: str
    images: List[Image]
    languages: List[str]
    name: str
    release_date: str
    release_date_precision: ReleaseDatePrecision
    resume_point: ResumePoint

    def __post_init__(self):
        self.images = ModelList(Image.from_kwargs(i) for i in self.images)
        self.release_date_precision = ReleaseDatePrecision[
            self.release_date_precision
        ]
        self.resume_point = ResumePoint.from_kwargs(self.resume_point)
