from __future__ import annotations

from datetime import datetime

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

    copyrights: list[Copyright]
    external_ids: dict
    genres: list[str]
    label: str | None
    popularity: int
    tracks: SimpleTrackPaging


class SavedAlbum(Model):
    """Album saved to library."""

    added_at: datetime
    album: FullAlbum


class SavedAlbumPaging(OffsetPaging):
    """Paging of albums in library."""

    items: list[SavedAlbum]
