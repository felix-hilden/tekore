from dataclasses import dataclass
from typing import List, Optional

from .base import Item
from .member import Image, ReleaseDatePrecision, ResumePoint
from .paging import OffsetPaging
from .serialise import Model, ModelList, Timestamp
from .show import SimpleShow


@dataclass(repr=False)
class Episode(Item):
    """Episode base."""

    audio_preview_url: str
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

    def __post_init__(self):
        self.images = ModelList(Image.from_kwargs(i) for i in self.images)
        self.languages = ModelList(self.languages)
        self.release_date_precision = ReleaseDatePrecision[self.release_date_precision]


@dataclass(repr=False)
class SimpleEpisode(Episode):
    """Simplified episode object."""

    resume_point: Optional[ResumePoint] = None

    def __post_init__(self):
        super().__post_init__()
        if self.resume_point is not None:
            self.resume_point = ResumePoint.from_kwargs(self.resume_point)


@dataclass(repr=False)
class FullEpisode(Episode):
    """Complete episode object."""

    show: SimpleShow
    resume_point: Optional[ResumePoint] = None

    def __post_init__(self):
        super().__post_init__()
        self.show = SimpleShow.from_kwargs(self.show)
        if self.resume_point is not None:
            self.resume_point = ResumePoint.from_kwargs(self.resume_point)


@dataclass(repr=False)
class SimpleEpisodePaging(OffsetPaging):
    """Paging of simplified episodes."""

    items = List[SimpleEpisode]

    def __post_init__(self):
        self.items = ModelList(
            SimpleEpisode.from_kwargs(i) if i is not None else None for i in self.items
        )


@dataclass(repr=False)
class SavedEpisode(Model):
    """Episode saved to library."""

    added_at: Timestamp
    episode: FullEpisode

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.episode = FullEpisode.from_kwargs(self.episode)


@dataclass(repr=False)
class SavedEpisodePaging(OffsetPaging):
    """Paging of episodes in library."""

    items: List[SavedEpisode]

    def __post_init__(self):
        self.items = ModelList(SavedEpisode.from_kwargs(a) for a in self.items)
