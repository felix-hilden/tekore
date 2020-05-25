from dataclasses import dataclass
from .serialise import Model, StrEnum


class ContextType(StrEnum):
    """Type of player context."""

    album = 'album'
    artist = 'artist'
    playlist = 'playlist'
    show = 'show'


@dataclass(repr=False)
class Context(Model):
    """Context of a played track or episode."""

    type: ContextType
    href: str
    external_urls: dict
    uri: str

    def __post_init__(self):
        self.type = ContextType[self.type]
