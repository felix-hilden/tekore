from typing import List
from dataclasses import dataclass

from spotipy.model.album.base import Album
from spotipy.model.member import Copyright, ExternalID
from spotipy.model.track import SimpleTrackPaging


@dataclass
class FullAlbum(Album):
    copyrights: List[Copyright]
    external_ids: ExternalID
    genres: List[str]
    label: str
    popularity: int
    tracks: SimpleTrackPaging
