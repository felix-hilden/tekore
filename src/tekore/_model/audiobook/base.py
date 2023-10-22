from typing import List, Optional

from ..base import Item
from ..member import Copyright, Image
from ..serialise import Model


class Author(Model):
    """Audiobook author."""

    name: str


class Narrator(Model):
    """Audiobook narrator."""

    name: str


class Audiobook(Item):
    """Audiobook base."""

    authors: List[Author]
    available_markets: Optional[List[str]] = None
    copyrights: List[Copyright]
    description: str
    edition: Optional[str]
    explicit: bool
    external_urls: dict
    html_description: str
    images: List[Image]
    is_externally_hosted: Optional[bool] = None
    languages: List[str]
    media_type: str
    name: str
    narrators: List[Narrator]
    publisher: str
    total_chapters: Optional[int]
