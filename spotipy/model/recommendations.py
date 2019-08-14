from enum import Enum
from typing import List
from dataclasses import dataclass

from spotipy.model.track import SimpleTrack

RecommendationType = Enum('RecommendationType', 'artist track genre')


@dataclass
class RecommendationSeed:
    after_filtering_size: int
    after_relinking_size: int
    href: str
    id: str
    initial_pool_size: int
    type: str


@dataclass
class Recommendations:
    seeds: List[RecommendationSeed]
    tracks: List[SimpleTrack]
