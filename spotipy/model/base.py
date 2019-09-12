from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


@dataclass
class Identifiable(SerialisableDataclass):
    id: str

    def __str__(self):
        return self.id


@dataclass
class Item(Identifiable):
    href: str
    type: str
    uri: str
