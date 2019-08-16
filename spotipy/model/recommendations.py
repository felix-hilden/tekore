from typing import List
from dataclasses import dataclass

from spotipy.model.track import SimpleTrack


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

    def __post_init__(self):
        self.seeds = [RecommendationSeed(**s) for s in self.seeds]
        self.tracks = [SimpleTrack(**t) for t in self.tracks]
