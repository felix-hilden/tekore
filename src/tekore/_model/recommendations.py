from typing import List, Optional

from .base import Identifiable
from .serialise import Model, StrEnum
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


class RecommendationSeed(Identifiable):
    """Recommendation seeds."""

    afterFilteringSize: int
    afterRelinkingSize: int
    href: Optional[str]
    initialPoolSize: int
    type: str


class Recommendations(Model):
    """Track recommendations."""

    seeds: List[RecommendationSeed]
    tracks: List[FullTrack]
