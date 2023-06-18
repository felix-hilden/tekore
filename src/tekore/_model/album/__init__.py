from typing import List, Optional

from ..album.base import Album, AlbumType
from ..paging import OffsetPaging
from ..serialise import StrEnum


class AlbumGroup(StrEnum):
    """Relationship between artist and album."""

    album = "album"
    appears_on = "appears_on"
    compilation = "compilation"
    single = "single"


class SimpleAlbum(Album):
    """
    Simplified album object.

    :attr:`album_group` is available when getting an artist's albums.
    :attr:`available_markets` is available when market is not specified.

    The presence of :attr:`is_playable` is undocumented
    and it appears to only be ``True`` when it is present.
    """

    album_group: Optional[AlbumGroup] = None


class SimpleAlbumPaging(OffsetPaging):
    """Paging containing simplified albums."""

    items: List[SimpleAlbum]
