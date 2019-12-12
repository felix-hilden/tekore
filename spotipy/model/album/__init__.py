from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableEnum
from spotipy.model.paging import OffsetPaging
from spotipy.model.album.base import Album


class AlbumGroup(SerialisableEnum):
    album = 'album',
    appears_on = 'appears_on',
    compilation = 'compilation',
    single = 'single',


@dataclass
class SimpleAlbum(Album):
    """
    Album group is available when getting an artist's albums.
    Available markets is available when market is not specified.

    The presence of is_playable is undocumented
    and it appears to only be True when it is present.
    """
    album_group: AlbumGroup = None
    available_markets: List[str] = None
    is_playable: True = None

    def __post_init__(self):
        super().__post_init__()
        if self.album_group is not None:
            self.album_group = AlbumGroup[self.album_group]


@dataclass
class SimpleAlbumPaging(OffsetPaging):
    items: List[SimpleAlbum]

    def __post_init__(self):
        self.items = [SimpleAlbum(**a) for a in self.items]
