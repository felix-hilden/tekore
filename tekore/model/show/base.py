from typing import List
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.member import Copyright, Image


@dataclass(repr=False)
class Show(Item):
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

    def __post_init__(self):
        self.copyrights = [Copyright(**c) for c in self.copyrights]
        self.images = [Image(**i) for i in self.images]
