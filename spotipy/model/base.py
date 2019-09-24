from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


@dataclass
class Identifiable(SerialisableDataclass):
    id: str


@dataclass
class Item(Identifiable):
    href: str
    type: str
    uri: str
