from dataclasses import dataclass
from tekore.serialise import SerialisableDataclass, SerialisableEnum


class ContextType(SerialisableEnum):
    album = 'album'
    artist = 'artist'
    playlist = 'playlist'


@dataclass(repr=False)
class Context(SerialisableDataclass):
    type: ContextType
    href: str
    external_urls: dict
    uri: str

    def __post_init__(self):
        self.type = ContextType[self.type]
