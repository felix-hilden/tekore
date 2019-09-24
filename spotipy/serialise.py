"""
Provide serialisation for models via the `str` function.
"""

import json

from enum import Enum
from dataclasses import dataclass, asdict


class JSONEncoder(json.JSONEncoder):
    """
    JSON Encoder capable of serialising enumerations.
    """
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        else:
            return super().default(o)


@dataclass
class SerialisableDataclass:
    """
    Convert dataclasses to JSON strings recursively.
    """
    def __str__(self):
        return JSONEncoder().encode(asdict(self))


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
