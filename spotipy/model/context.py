from dataclasses import dataclass


@dataclass
class Context:
    type: str
    href: str
    external_urls: dict
    uri: str
