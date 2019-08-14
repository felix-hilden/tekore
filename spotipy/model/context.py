from dataclasses import dataclass

from spotipy.model.member import ExternalURL


@dataclass
class Context:
    type: str
    href: str
    external_urls: ExternalURL
    uri: str
