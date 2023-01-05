from dataclasses import dataclass
from typing import List, Optional

from ..base import Item
from ..member import Copyright, Image
from ..serialise import ModelList


@dataclass(repr=False)
class Show(Item):
    """Show base."""

    available_markets: List[str]
    copyrights: List[Copyright]
    description: str
    explicit: bool
    external_urls: dict
    images: List[Image]
    is_externally_hosted: bool
    languages: List[str]
    media_type: str
    name: str
    publisher: str
    total_episodes: Optional[int] = None
    html_description: str = None

    def __post_init__(self):
        self.available_markets = ModelList(self.available_markets)
        self.copyrights = ModelList(Copyright.from_kwargs(c) for c in self.copyrights)
        self.images = ModelList(Image.from_kwargs(i) for i in self.images)
        self.languages = ModelList(self.languages)
