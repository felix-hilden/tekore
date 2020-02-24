from typing import List
from dataclasses import dataclass
from tekore.serialise import SerialisableDataclass


@dataclass(repr=False)
class TimeInterval(SerialisableDataclass):
    start: float
    duration: float
    confidence: float


@dataclass(repr=False)
class Section(TimeInterval):
    loudness: float
    tempo: float
    tempo_confidence: float
    key: int
    key_confidence: float
    mode: int
    mode_confidence: float
    time_signature: int
    time_signature_confidence: float


@dataclass(repr=False)
class Segment(TimeInterval):
    """
    Loudness end is sometimes not available.
    """
    loudness_start: float
    loudness_max: float
    loudness_max_time: float
    pitches: List[float]
    timbre: List[float]
    loudness_end: float = None


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
