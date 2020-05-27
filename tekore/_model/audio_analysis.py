from typing import List
from dataclasses import dataclass
from .serialise import Model, ModelList


@dataclass(repr=False)
class TimeInterval(Model):
    """
    Generic representation of an interval.

    Attributes are sometimes not available.
    """

    duration: float
    start: float = None
    confidence: float = None


@dataclass(repr=False)
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
    confidence: float = None
    mode: int = None
    key: int = None
    start: float = None


@dataclass(repr=False)
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
    confidence: float = None
    loudness_end: float = None
    loudness_max_time: float = None
    start: float = None

    def __post_init__(self):
        self.pitches = ModelList(self.pitches)
        self.timbre = ModelList(self.timbre)


@dataclass(repr=False)
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

    def __post_init__(self):
        self.bars = ModelList(TimeInterval(**i) for i in self.bars)
        self.beats = ModelList(TimeInterval(**i) for i in self.beats)
        self.sections = ModelList(Section(**s) for s in self.sections)
        self.segments = ModelList(Segment(**s) for s in self.segments)
        self.tatums = ModelList(TimeInterval(**i) for i in self.tatums)
