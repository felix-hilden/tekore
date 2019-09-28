from enum import Enum
from dataclasses import dataclass
from spotipy.model.base import Identifiable

DeviceType = Enum(
    'DeviceType',
    'Computer Tablet Smartphone Speaker TV AVR STB AudioDongle '
    'GameConsole CastVideo CastAudio Automobile Unknown'
)


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
