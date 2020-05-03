from typing import List
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.show import SimpleShow
from tekore.model.paging import OffsetPaging
from tekore.model.member import Image, ReleaseDatePrecision
from tekore.model.serialise import Model, ModelList


@dataclass(repr=False)
class ResumePoint(Model):
    fully_played: bool
    resume_position_ms: int


@dataclass(repr=False)
class Episode(Item):
    audio_preview_url: str
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict
    images: List[Image]
    is_externally_hosted: bool
    is_playable: bool
    language: str
    languages: List[str]
    name: str
    release_date: str
    release_date_precision: ReleaseDatePrecision

    def __post_init__(self):
        self.images = ModelList(Image(**i) for i in self.images)
        self.languages = ModelList(self.languages)
        self.release_date_precision = ReleaseDatePrecision[
            self.release_date_precision
        ]


@dataclass(repr=False)
class SimpleEpisode(Episode):
    resume_point: ResumePoint = None

    def __post_init__(self):
        super().__post_init__()
        if self.resume_point is not None:
            self.resume_point = ResumePoint(**self.resume_point)


@dataclass(repr=False)
class FullEpisode(Episode):
    """
    Episode and track are only available on a playlist.
    """
    show: SimpleShow
    episode: bool = None
    track: bool = None
    resume_point: ResumePoint = None

    def __post_init__(self):
        super().__post_init__()
        self.show = SimpleShow(**self.show)
        if self.resume_point is not None:
            self.resume_point = ResumePoint(**self.resume_point)


@dataclass(repr=False)
class SimpleEpisodePaging(OffsetPaging):
    items = List[SimpleEpisode]

    def __post_init__(self):
        self.items = ModelList(
            SimpleEpisode(**i) if i is not None else None
            for i in self.items
        )
