from dataclasses import dataclass
from datetime import datetime

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
    key: str
    value: str


@dataclass
class Timestamp:
    datetime: datetime

    def __post_init__(self):
        self.datetime = datetime.strptime(
            self.datetime, '%Y-%m-%dT%H:%M:%S%z'
        )

    def __str__(self):
        return self.datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
