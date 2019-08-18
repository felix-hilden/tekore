from dataclasses import dataclass
from datetime import datetime


@dataclass
class Copyright:
    text: str
    type: str


@dataclass
class Followers:
    href: str
    total: int


@dataclass
class Image:
    url: str
    height: int = None
    width: int = None


@dataclass
class Restrictions:
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
