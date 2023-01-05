from dataclasses import dataclass
from typing import List

from .base import Identifiable
from .serialise import Model, ModelList, StrEnum
from .track import FullTrack


class RecommendationAttribute(StrEnum):
    """Attributes available in recommendations."""

    acousticness = "acousticness"
    danceability = "danceability"
    duration_ms = "duration_ms"
    energy = "energy"
    instrumentalness = "instrumentalness"
    key = "key"
    liveness = "liveness"
    loudness = "loudness"
    mode = "mode"
    popularity = "popularity"
    speechiness = "speechiness"
    tempo = "tempo"
    time_signature = "time_signature"
    valence = "valence"


@dataclass(repr=False)
class RecommendationSeed(Identifiable):
    """Recommendation seeds."""

    afterFilteringSize: int
    afterRelinkingSize: int
    href: str
    initialPoolSize: int
    type: str


@dataclass(repr=False)
class Recommendations(Model):
    """Track recommendations."""

    seeds: List[RecommendationSeed]
    tracks: List[FullTrack]

    def __post_init__(self):
        self.seeds = ModelList(RecommendationSeed.from_kwargs(s) for s in self.seeds)
        self.tracks = ModelList(FullTrack.from_kwargs(t) for t in self.tracks)
