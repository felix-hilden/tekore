from typing import Optional
from dataclasses import dataclass

from tekore.model.base import Identifiable
from tekore.model.serialise import StrEnum


class DeviceType(StrEnum):
    Computer = 'Computer'
    Tablet = 'Tablet'
    Smartphone = 'Smartphone'
    Speaker = 'Speaker'
    TV = 'TV'
    AVR = 'AVR'
    STB = 'STB'
    AudioDongle = 'AudioDongle'
    GameConsole = 'GameConsole'
    CastVideo = 'CastVideo'
    CastAudio = 'CastAudio'
    Automobile = 'Automobile'
    Unknown = 'Unknown'


@dataclass(repr=False)
class Device(Identifiable):
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: DeviceType
    volume_percent: Optional[int]

    def __post_init__(self):
        self.type = DeviceType[self.type]
