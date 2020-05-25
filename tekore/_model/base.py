from dataclasses import dataclass
from .serialise import Model


@dataclass(repr=False)
class Identifiable(Model):
    """Object identified with a Spotify ID."""

    id: str


@dataclass(repr=False)
class Item(Identifiable):
    """Identifiable with additional fields."""

    href: str
    type: str
    uri: str
