"""
Provide serialisation for models via the `str` function.
"""

import json

from enum import Enum
from dataclasses import dataclass, asdict


class SerialisableEnum(Enum):
    """
    Convert enumeration members to strings using their name.
    """
    def __str__(self):
        return self.name


@dataclass
class SerialisableDataclass:
    """
    Convert dataclasses to JSON strings recursively.
    """
    def __str__(self):
        return json.dumps(asdict(self))


class ModelList(list):
    """
    List that calls `str` instead of the default `repr` on its members
    in its `__str__` method.

    This is done to allow for easy serialisation of lists of models
    (without defining a custom JSON serialiser)
    while keeping the `repr` of models still available.
    """
    def __str__(self):
        return '[' + ', '.join(str(model) for model in self) + ']'
