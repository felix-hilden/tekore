from .base import Identifiable
from .member import Image
from .paging import OffsetPaging


class Category(Identifiable):
    """Spotify tag category."""

    href: str
    icons: list[Image]
    name: str


class CategoryPaging(OffsetPaging):
    """Paging of categories."""

    items: list[Category]
