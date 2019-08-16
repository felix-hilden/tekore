from typing import List
from dataclasses import dataclass

from spotipy.model.base import Identifiable
from spotipy.model.member import Image


@dataclass
class Category(Identifiable):
    href: str
    icons: List[Image]
    name: str

    def __post_init__(self):
        self.icons = [Image(**i) for i in self.icons]
