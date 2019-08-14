from enum import Enum
from dataclasses import dataclass

from spotipy.model.album.base import Album, AlbumType, ReleaseDatePrecision

AlbumGroup = Enum('AlbumGroup', 'album single compilation appears_on')


@dataclass
class SimpleAlbum(Album):
    album_group: AlbumGroup = None


@dataclass
class SavedAlbum:
    added_at: str
    album: Album
