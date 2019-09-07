from enum import Enum


class SerialisableEnum(Enum):
    """
    Convert enumeration members to strings using their name.
    """
    def __str__(self):
        return self.name
