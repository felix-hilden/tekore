from dataclasses import dataclass
from tekore.model.serialise import Model


@dataclass(repr=False)
class Identifiable(Model):
    id: str


@dataclass(repr=False)
class Item(Identifiable):
    href: str
    type: str
    uri: str
