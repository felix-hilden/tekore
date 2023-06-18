from .serialise import Model, StrEnum


class ContextType(StrEnum):
    """Type of player context."""

    album = "album"
    artist = "artist"
    collection = "collection"
    playlist = "playlist"
    show = "show"


class Context(Model):
    """Context of a played track or episode."""

    type: ContextType
    href: str
    external_urls: dict
    uri: str
