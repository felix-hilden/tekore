from typing import List
from dataclasses import dataclass

from tekore.serialise import SerialisableDataclass


class EmptyList(list):
    pass


class EmptyDict(dict):
    pass


@dataclass(repr=False)
class LocalItem(SerialisableDataclass):
    id: None
    href: None
    name: str
    type: str
    uri: None


@dataclass(repr=False)
class LocalAlbum(LocalItem):
    album_type: None
    artists: EmptyList
    available_markets: EmptyList
    external_urls: EmptyDict
    images: EmptyList
    release_date: None
    release_date_precision: None


@dataclass(repr=False)
class LocalArtist(LocalItem):
    external_urls: EmptyDict


@dataclass(repr=False)
class LocalTrack(LocalItem):
    album: LocalAlbum
    artists: List[LocalArtist]
    available_markets: EmptyList
    disc_number: 0
    duration_ms: int
    explicit: False
    external_ids: EmptyDict
    external_urls: EmptyDict
    is_local: True
    popularity: 0
    preview_url: None
    track_number: 0
    uri: str

    def __post_init__(self):
        self.album = LocalAlbum(**self.album)
        self.artists = [LocalArtist(**a) for a in self.artists]
