from typing import List, Optional

from .serialise import Model


class TimeInterval(Model):
    """
    Generic representation of an interval.

    Attributes are sometimes not available.
    """

    duration: float
    start: Optional[float] = None
    confidence: Optional[float] = None


class Section(Model):
    """
    Analysis of a track's section.

    Attributes are sometimes not available.
    """

    duration: float
    loudness: float
    tempo: float
    tempo_confidence: float
    key_confidence: float
    mode_confidence: float
    time_signature: int
    time_signature_confidence: float
    confidence: Optional[float] = None
    mode: Optional[int] = None
    key: Optional[int] = None
    start: Optional[float] = None


class Segment(Model):
    """
    Analysis of a track's segment.

    Attributes are sometimes not available.
    """

    duration: float
    loudness_start: float
    loudness_max: float
    pitches: List[float]
    timbre: List[float]
    confidence: Optional[float] = None
    loudness_end: Optional[float] = None
    loudness_max_time: Optional[float] = None
    start: Optional[float] = None


class AudioAnalysis(Model):
    """
    Track audio analysis.

    See the Web API
    `documentation <https://developer.spotify.com/documentation/web-api/\
    reference/tracks/get-audio-analysis/>`_
    for more details.
    """

    bars: List[TimeInterval]
    beats: List[TimeInterval]
    sections: List[Section]
    segments: List[Segment]
    tatums: List[TimeInterval]
    meta: dict
    track: dict
