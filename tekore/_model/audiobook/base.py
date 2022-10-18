from typing import List
from dataclasses import dataclass

from ..base import Item
from ..member import Copyright, Image
from ..serialise import ModelList, Model


@dataclass(repr=False)
class Author(Model):
    """Audiobook author."""

    name: str


@dataclass(repr=False)
class Narrator(Model):
    """Audiobook narrator."""

    name: str


@dataclass(repr=False)
class Audiobook(Item):
    """Audiobook base."""

    authors: List[Author]
    copyrights: List[Copyright]
    description: str
    edition: str
    explicit: bool
    external_urls: dict
    html_description: str
    images: List[Image]
    languages: List[str]
    media_type: str
    name: str
    narrators: List[Narrator]
    publisher: str
    total_chapters: int

    def __post_init__(self):
        self.authors = ModelList(Author(**i) for i in self.authors)
        self.copyrights = ModelList(Copyright(**i) for i in self.copyrights)
        self.images = ModelList(Image(**i) for i in self.images)
        self.narrators = ModelList(Narrator(**i) for i in self.narrators)
