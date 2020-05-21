from typing import List
from dataclasses import dataclass

from ..paging import OffsetPaging
from ..serialise import StrEnum, ModelList
from ..album.base import Album, AlbumType


class AlbumGroup(StrEnum):
    """
    Relationship between artist and album.
    """
    album = 'album'
    appears_on = 'appears_on'
    compilation = 'compilation'
    single = 'single'


@dataclass(repr=False)
class SimpleAlbum(Album):
    """
    Simplified album object.

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
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)


@dataclass(repr=False)
class SimpleAlbumPaging(OffsetPaging):
    """
    Paging containing simplified albums.
    """
    items: List[SimpleAlbum]

    def __post_init__(self):
        self.items = ModelList(SimpleAlbum(**a) for a in self.items)
