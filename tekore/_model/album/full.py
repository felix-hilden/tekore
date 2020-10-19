from typing import List, Optional
from dataclasses import dataclass

from ..track import SimpleTrackPaging
from ..member import Copyright
from ..paging import OffsetPaging
from ..serialise import Model, ModelList, Timestamp
from ..album.base import Album


@dataclass(repr=False)
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
    label: str
    popularity: int
    tracks: SimpleTrackPaging
    available_markets: Optional[List[str]] = None
    is_playable: Optional[bool] = None

    def __post_init__(self):
        super().__post_init__()
        if self.available_markets is not None:
            self.available_markets = ModelList(self.available_markets)
        self.copyrights = ModelList(Copyright(**c) for c in self.copyrights)
        self.genres = ModelList(self.genres)
        self.tracks = SimpleTrackPaging(**self.tracks)


@dataclass(repr=False)
class SavedAlbum(Model):
    """Album saved to library."""

    added_at: Timestamp
    album: FullAlbum

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.album = FullAlbum(**self.album)


@dataclass(repr=False)
class SavedAlbumPaging(OffsetPaging):
    """Paging of albums in library."""

    items: List[SavedAlbum]

    def __post_init__(self):
        self.items = ModelList(SavedAlbum(**a) for a in self.items)
