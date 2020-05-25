from typing import List
from dataclasses import dataclass

from .base import Identifiable
from .track import FullTrack
from .serialise import Model, ModelList, StrEnum


class RecommendationAttribute(StrEnum):
    """Attributes available in recommendations."""

    acousticness = 'acousticness'
    danceability = 'danceability'
    duration_ms = 'duration_ms'
    energy = 'energy'
    instrumentalness = 'instrumentalness'
    key = 'key'
    liveness = 'liveness'
    loudness = 'loudness'
    mode = 'mode'
    popularity = 'popularity'
    speechiness = 'speechiness'
    tempo = 'tempo'
    time_signature = 'time_signature'
    valence = 'valence'


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
        self.seeds = ModelList(RecommendationSeed(**s) for s in self.seeds)
        self.tracks = ModelList(FullTrack(**t) for t in self.tracks)
