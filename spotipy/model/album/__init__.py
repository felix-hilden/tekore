from enum import Enum
from dataclasses import dataclass

from spotipy.model.album.base import Album, AlbumType, ReleaseDatePrecision

AlbumGroup = Enum('AlbumGroup', 'album single compilation appears_on')


@dataclass
class SimpleAlbum(Album):
    album_group: AlbumGroup = None

    def __post_init__(self):
        super().__post_init__()
        self.album_group = AlbumGroup[self.album_group] if self.album_group is not None else None


@dataclass
class SavedAlbum:
    added_at: str
    album: Album

    def __post_init__(self):
        self.album = Album(**self.album)
