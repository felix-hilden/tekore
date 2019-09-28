from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableDataclass
from spotipy.model.album.base import Album
from spotipy.model.member import Copyright, Restrictions, Timestamp
from spotipy.model.track import SimpleTrackPaging
from spotipy.model.paging import OffsetPaging


@dataclass
class FullAlbum(Album):
    copyrights: List[Copyright]
    external_ids: dict
    genres: List[str]
    label: str
    popularity: int
    tracks: SimpleTrackPaging
    is_playable: bool = None
    available_markets: List[str] = None
    restrictions: Restrictions = None

    def __post_init__(self):
        super().__post_init__()
        self.copyrights = [Copyright(**c) for c in self.copyrights]
        self.tracks = SimpleTrackPaging(**self.tracks)
        if self.restrictions is not None:
            self.restrictions = Restrictions(**self.restrictions)


@dataclass
class SavedAlbum(SerialisableDataclass):
    added_at: Timestamp
    album: FullAlbum

    def __post_init__(self):
        self.added_at = Timestamp(datetime=self.added_at)
        self.album = FullAlbum(**self.album)


@dataclass
class SavedAlbumPaging(OffsetPaging):
    items: List[SavedAlbum]

    def __post_init__(self):
        self.items = [SavedAlbum(**a) for a in self.items]
