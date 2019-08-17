from dataclasses import dataclass


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
