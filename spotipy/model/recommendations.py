from typing import List
from dataclasses import dataclass

from spotipy.model.base import Identifiable
from spotipy.model.track import FullTrack
from spotipy.serialise import SerialisableDataclass, SerialisableEnum


class RecommendationAttribute(SerialisableEnum):
    acousticness = 'acousticness',
    danceability = 'danceability',
    duration_ms = 'duration_ms',
    energy = 'energy',
    instrumentalness = 'instrumentalness',
    key = 'key',
    liveness = 'liveness',
    loudness = 'loudness',
    mode = 'mode',
    popularity = 'popularity',
    speechiness = 'speechiness',
    tempo = 'tempo',
    time_signature = 'time_signature',
    valence = 'valence'


@dataclass
class RecommendationSeed(Identifiable):
    afterFilteringSize: int
    afterRelinkingSize: int
    href: str
    initialPoolSize: int
    type: str


@dataclass
class Recommendations(SerialisableDataclass):
    seeds: List[RecommendationSeed]
    tracks: List[FullTrack]

    def __post_init__(self):
        self.seeds = [RecommendationSeed(**s) for s in self.seeds]
        self.tracks = [FullTrack(**t) for t in self.tracks]
