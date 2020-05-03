from dataclasses import dataclass
from tekore.model.serialise import Model, StrEnum


class ContextType(StrEnum):
    album = 'album'
    artist = 'artist'
    playlist = 'playlist'
    show = 'show'


@dataclass(repr=False)
class Context(Model):
    type: ContextType
    href: str
    external_urls: dict
    uri: str

    def __post_init__(self):
        self.type = ContextType[self.type]
