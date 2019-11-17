from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


@dataclass
class Copyright(SerialisableDataclass):
    text: str
    type: str


@dataclass
class Followers(SerialisableDataclass):
    """
    Href is always None.
    """
    href: None
    total: int


@dataclass
class Image(SerialisableDataclass):
    """
    The Web API documentation reports that height and width
    can be None or not available in the response.
    """
    url: str
    height: int = None
    width: int = None


@dataclass
class Restrictions(SerialisableDataclass):
    reason: str
