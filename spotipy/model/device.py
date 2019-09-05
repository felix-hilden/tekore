from dataclasses import dataclass
from spotipy.model.base import Identifiable


@dataclass
class Device(Identifiable):
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    volume_percent: int = None
