from .base import Identifiable


class AudioFeatures(Identifiable):
    """Features of a track."""

    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    track_href: str
    type: str
    uri: str
    valence: float
