from typing import List, Optional
from dataclasses import dataclass

from ..paging import OffsetPaging
from ..serialise import StrEnum, ModelList
from ..album.base import Album, AlbumType


class AlbumGroup(StrEnum):
    """Relationship between artist and album."""

    album = 'album'
    appears_on = 'appears_on'
    compilation = 'compilation'
    single = 'single'


@dataclass(repr=False)
class SimpleAlbum(Album):
    """
    Simplified album object.

    :attr:`album_group` is available when getting an artist's albums.
    :attr:`available_markets` is available when market is not specified.

    The presence of :attr:`is_playable` is undocumented
    and it appears to only be ``True`` when it is present.
    """

    album_group: Optional[AlbumGroup] = None
    available_markets: Optional[List[str]] = None
    is_playable: Optional[bool] = None

    def __post_init__(self):
        super().__post_init__()
        if self.album_group is not None:
            self.album_group = AlbumGroup[self.album_group]
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)


@dataclass(repr=False)
class SimpleAlbumPaging(OffsetPaging):
    """Paging containing simplified albums."""

    items: List[SimpleAlbum]

    def __post_init__(self):
        self.items = ModelList(SimpleAlbum(**a) for a in self.items)
