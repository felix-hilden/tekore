from dataclasses import dataclass
from tekore.serialise import SerialisableDataclass, SerialisableEnum


class ReleaseDatePrecision(SerialisableEnum):
    year = 'year'
    month = 'month'
    day = 'day'


@dataclass(repr=False)
class Copyright(SerialisableDataclass):
    text: str
    type: str


@dataclass(repr=False)
class Followers(SerialisableDataclass):
    """
    Href is always None.
    """
    href: None
    total: int


@dataclass(repr=False)
class Image(SerialisableDataclass):
    """
    The Web API documentation reports that height and width
    can be None or not available in the response.
    """
    url: str
    height: int = None
    width: int = None


@dataclass(repr=False)
class Restrictions(SerialisableDataclass):
    reason: str
