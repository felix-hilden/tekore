from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


@dataclass
class Copyright(SerialisableDataclass):
    text: str
    type: str


@dataclass
class Followers(SerialisableDataclass):
    href: str
    total: int


@dataclass
class Image(SerialisableDataclass):
    url: str
    height: int = None
    width: int = None


@dataclass
class Restrictions(SerialisableDataclass):
    reason: str
