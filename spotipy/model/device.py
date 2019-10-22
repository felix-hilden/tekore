from enum import Enum
from dataclasses import dataclass
from spotipy.model.base import Identifiable


class DeviceType(Enum):
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


@dataclass
class Device(Identifiable):
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: DeviceType
    volume_percent: int = None

    def __post_init__(self):
        self.type = DeviceType[self.type]
