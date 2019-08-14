from dataclasses import dataclass


@dataclass
class Identifiable:
    id: str

    def __str__(self):
        return self.id


@dataclass
class Item(Identifiable):
    href: str
    type: str
    uri: str
