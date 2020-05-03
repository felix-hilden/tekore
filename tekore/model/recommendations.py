from typing import List
from dataclasses import dataclass

from tekore.model.base import Identifiable
from tekore.model.track import FullTrack
from tekore.model.serialise import Model, ModelList, StrEnum


class RecommendationAttribute(StrEnum):
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
    afterFilteringSize: int
    afterRelinkingSize: int
    href: str
    initialPoolSize: int
    type: str


@dataclass(repr=False)
class Recommendations(Model):
    seeds: List[RecommendationSeed]
    tracks: List[FullTrack]

    def __post_init__(self):
        self.seeds = ModelList(RecommendationSeed(**s) for s in self.seeds)
        self.tracks = ModelList(FullTrack(**t) for t in self.tracks)
