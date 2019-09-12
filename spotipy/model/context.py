from dataclasses import dataclass
from spotipy.serialise import SerialisableDataclass


@dataclass
class Context(SerialisableDataclass):
    type: str
    href: str
    external_urls: dict
    uri: str
