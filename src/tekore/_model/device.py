from __future__ import annotations

from .base import Identifiable
from .serialise import StrEnum


class DeviceType(StrEnum):
    """Type of playback device."""

    Computer = "Computer"
    Tablet = "Tablet"
    Smartphone = "Smartphone"
    Speaker = "Speaker"
    TV = "TV"
    AVR = "AVR"
    STB = "STB"
    AudioDongle = "AudioDongle"
    GameConsole = "GameConsole"
    CastVideo = "CastVideo"
    CastAudio = "CastAudio"
    Automobile = "Automobile"
    Unknown = "Unknown"


class Device(Identifiable):
    """Playback device."""

    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: DeviceType
    volume_percent: int | None
    supports_volume: bool
