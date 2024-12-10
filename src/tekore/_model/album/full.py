from __future__ import annotations

from datetime import datetime

from tekore._model.album.base import Album
from tekore._model.member import Copyright
from tekore._model.paging import OffsetPaging
from tekore._model.serialise import Model
from tekore._model.track import SimpleTrackPaging


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
