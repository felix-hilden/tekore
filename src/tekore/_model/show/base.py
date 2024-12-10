from __future__ import annotations

from pydantic import Field

from tekore._model.base import Item
from tekore._model.member import Copyright, Image


class Show(Item):
    """
    Show base.

    :attr:`publisher` being an object is undocumented.
    """

    available_markets: list[str] = Field(default_factory=list)
    copyrights: list[Copyright]
    description: str
    explicit: bool
    external_urls: dict
    html_description: str | None = None
    images: list[Image]
    is_externally_hosted: bool | None
    languages: list[str]
    media_type: str
    name: str
    publisher: str | dict
    total_episodes: int | None = None
