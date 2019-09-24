from enum import Enum
from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableDataclass
from spotipy.model.member import Timestamp, Restrictions
from spotipy.model.paging import OffsetPaging
from spotipy.model.album.base import Album, AlbumType, ReleaseDatePrecision

AlbumGroup = Enum('AlbumGroup', 'album single compilation appears_on')


@dataclass
class SimpleAlbum(Album):
    album_group: AlbumGroup = None
    available_markets: List[str] = None
    restrictions: Restrictions = None

    def __post_init__(self):
        super().__post_init__()
        if self.album_group is not None:
            self.album_group = AlbumGroup[self.album_group]
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass
class SimpleAlbumPaging(OffsetPaging):
    items: List[SimpleAlbum]

    def __post_init__(self):
        self.items = [SimpleAlbum(**a) for a in self.items]


@dataclass
class SavedAlbum(SerialisableDataclass):
    added_at: Timestamp
    album: Album

    def __post_init__(self):
        self.added_at = Timestamp(datetime=self.added_at)
        self.album = Album(**self.album)


@dataclass
class SavedAlbumPaging(OffsetPaging):
    items: List[SavedAlbum]

    def __post_init__(self):
        self.items = [SavedAlbum(**a) for a in self.items]
