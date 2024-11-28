from __future__ import annotations

from .serialise import Model


class TimeInterval(Model):
    """
    Generic representation of an interval.

    Attributes are sometimes not available.
    """

    duration: float
    start: float | None = None
    confidence: float | None = None


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
    confidence: float | None = None
    mode: int | None = None
    key: int | None = None
    start: float | None = None


class Segment(Model):
    """
    Analysis of a track's segment.

    Attributes are sometimes not available.
    """

    duration: float
    loudness_start: float
    loudness_max: float
    pitches: list[float]
    timbre: list[float]
    confidence: float | None = None
    loudness_end: float | None = None
    loudness_max_time: float | None = None
    start: float | None = None


class AudioAnalysis(Model):
    """
    Track audio analysis.

    See the Web API
    `documentation <https://developer.spotify.com/documentation/web-api/\
    reference/tracks/get-audio-analysis/>`_
    for more details.
    """

    bars: list[TimeInterval]
    beats: list[TimeInterval]
    sections: list[Section]
    segments: list[Segment]
    tatums: list[TimeInterval]
    meta: dict
    track: dict
