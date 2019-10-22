from enum import Enum
from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


class ContextType(Enum):
    album = 'album'
    artist = 'artist'
    playlist = 'playlist'


@dataclass
class Context(SerialisableDataclass):
    type: ContextType
    href: str
    external_urls: dict
    uri: str

    def __post_init__(self):
        self.type = ContextType[self.type]
