from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableEnum
from spotipy.model.member import Restrictions
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
    Available markets are not available when market is specified.
    Is playable is not available when market is None.
    Restrictions is available if restrictions have been placed on
    the album, making it unplayable.
    """
    is_playable: bool = None
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
