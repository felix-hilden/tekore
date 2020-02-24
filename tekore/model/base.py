from dataclasses import dataclass
from tekore.serialise import SerialisableDataclass


@dataclass(repr=False)
class Identifiable(SerialisableDataclass):
    id: str


@dataclass(repr=False)
class Item(Identifiable):
    href: str
    type: str
    uri: str
