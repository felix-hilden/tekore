from .serialise import Model


class Identifiable(Model):
    """Object identified with a Spotify ID."""

    id: str


class Item(Identifiable):
    """Identifiable with additional fields."""

    href: str
    type: str
    uri: str
