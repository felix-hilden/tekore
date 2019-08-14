from enum import Enum
from dataclasses import dataclass

from spotipy.model.base import Identifiable

Key = Enum('Key', 'C C# D Eb E F F# G G# A Bb B')
Mode = Enum('Mode', 'minor major')


@dataclass
class AudioFeatures(Identifiable):
    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: Key
    liveness: float
    loudness: float
    mode: Mode
    speechiness: float
    tempo: float
    time_signature: int
    track_href: str
    type: str
    uri: str
    valence: float
