from dataclasses import dataclass
from .serialise import Model, StrEnum


class ReleaseDatePrecision(StrEnum):
    """Precision of a release date."""

    year = 'year'
    month = 'month'
    day = 'day'


@dataclass(repr=False)
class Copyright(Model):
    """Copyright."""

    text: str
    type: str


@dataclass(repr=False)
class Followers(Model):
    """
    Followers.

    Href is always None.
    """

    href: None
    total: int


@dataclass(repr=False)
class Image(Model):
    """
    Image link and information.

    The Web API documentation reports that height and width
    can be None or not available in the response.
    """

    url: str
    height: int = None
    width: int = None
