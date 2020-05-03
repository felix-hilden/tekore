from dataclasses import dataclass
from tekore.model.serialise import Model, StrEnum


class ReleaseDatePrecision(StrEnum):
    year = 'year'
    month = 'month'
    day = 'day'


@dataclass(repr=False)
class Copyright(Model):
    text: str
    type: str


@dataclass(repr=False)
class Followers(Model):
    """
    Href is always None.
    """
    href: None
    total: int


@dataclass(repr=False)
class Image(Model):
    """
    The Web API documentation reports that height and width
    can be None or not available in the response.
    """
    url: str
    height: int = None
    width: int = None


@dataclass(repr=False)
class Restrictions(Model):
    reason: str
