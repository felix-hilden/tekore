from dataclasses import dataclass

from spotipy.model.member import ExternalURL


@dataclass
class Context:
    type: str
    href: str
    external_urls: ExternalURL
    uri: str

    def __post_init__(self):
        self.external_urls = ExternalURL(**self.external_urls)
