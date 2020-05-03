from typing import List
from dataclasses import dataclass

from tekore.model.base import Identifiable
from tekore.model.member import Image
from tekore.model.paging import OffsetPaging
from tekore.model.serialise import ModelList


@dataclass(repr=False)
class Category(Identifiable):
    href: str
    icons: List[Image]
    name: str

    def __post_init__(self):
        self.icons = ModelList(Image(**i) for i in self.icons)


@dataclass(repr=False)
class CategoryPaging(OffsetPaging):
    items: List[Category]

    def __post_init__(self):
        self.items = ModelList(Category(**c) for c in self.items)
