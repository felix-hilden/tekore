from datetime import datetime
from typing import List, Optional

from ..album.base import Album
from ..member import Copyright
from ..paging import OffsetPaging
from ..serialise import Model
from ..track import SimpleTrackPaging


class FullAlbum(Album):
    """
    Complete album object.

    :attr:`available_markets` is available when market is not specified.

    The presence of :attr:`is_playable` is undocumented
    and it appears to only be ``True`` when it is present.
    """

    copyrights: List[Copyright]
    external_ids: dict
    genres: List[str]
    label: Optional[str]
    popularity: int
    tracks: SimpleTrackPaging


class SavedAlbum(Model):
    """Album saved to library."""

    added_at: datetime
    album: FullAlbum


class SavedAlbumPaging(OffsetPaging):
    """Paging of albums in library."""

    items: List[SavedAlbum]
