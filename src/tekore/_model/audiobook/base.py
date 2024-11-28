from __future__ import annotations

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

    authors: list[Author]
    available_markets: list[str] | None = None
    copyrights: list[Copyright]
    description: str
    edition: str | None
    explicit: bool
    external_urls: dict
    html_description: str
    images: list[Image]
    is_externally_hosted: bool | None = None
    languages: list[str]
    media_type: str
    name: str
    narrators: list[Narrator]
    publisher: str
    total_chapters: int | None
