from typing import List
from dataclasses import dataclass

from tekore.model.base import Identifiable
from tekore.model.member import Image
from tekore.model.paging import OffsetPaging


@dataclass
class Category(Identifiable):
    href: str
    icons: List[Image]
    name: str

    def __post_init__(self):
        self.icons = [Image(**i) for i in self.icons]


@dataclass
class CategoryPaging(OffsetPaging):
    items: List[Category]

    def __post_init__(self):
        self.items = [Category(**c) for c in self.items]
