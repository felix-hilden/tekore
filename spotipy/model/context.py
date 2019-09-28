from enum import Enum
from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass

ContextType = Enum('ContextType', 'album artist playlist')


@dataclass
class Context(SerialisableDataclass):
    type: ContextType
    href: str
    external_urls: dict
    uri: str

    def __post_init__(self):
        self.type = ContextType[self.type]
