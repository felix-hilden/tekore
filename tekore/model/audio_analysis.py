from typing import List
from dataclasses import dataclass
from tekore.serialise import SerialisableDataclass


@dataclass(repr=False)
class TimeInterval(SerialisableDataclass):
    """
    Attributes are sometimes not available.
    """
    duration: float
    start: float = None
    confidence: float = None


@dataclass(repr=False)
class Section(SerialisableDataclass):
    """
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
class Segment(SerialisableDataclass):
    """
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


@dataclass(repr=False)
class AudioAnalysis(SerialisableDataclass):
    bars: List[TimeInterval]
    beats: List[TimeInterval]
    sections: List[Section]
    segments: List[Segment]
    tatums: List[TimeInterval]
    meta: dict
    track: dict

    def __post_init__(self):
        self.bars = [TimeInterval(**i) for i in self.bars]
        self.beats = [TimeInterval(**i) for i in self.beats]
        self.sections = [Section(**s) for s in self.sections]
        self.segments = [Segment(**s) for s in self.segments]
        self.tatums = [TimeInterval(**i) for i in self.tatums]
