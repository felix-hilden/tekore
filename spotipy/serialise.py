"""
serialise
=========

Serialisation and convenience methods for models returned from the client.

The :class:`SerialisableDataclass` defined in this module along with other
supporting classes makes it possible to access the original representations
as dictionaries and JSON strings.
Easy inspection of the data contents is made possible by
the ``SerialisableDataclass.pprint`` function.

.. code:: python

    from spotipy import Spotify

    # Call the Web API
    spotify = Spotify(user_token)
    user = spotify.current_user()

    # Inspect the content
    user.pprint()

    # Original dict representation
    user.asdict()

    # Original representation as a string
    s = str(user)
"""

import json

from enum import Enum
from pprint import pprint
from datetime import datetime
from dataclasses import dataclass, asdict


class SerialisableEnum(Enum):
    """
    Convert enumeration members to strings using their name.
    """
    def __str__(self):
        return self.name


class Timestamp(datetime):
    """
    Timestamp whose string representation is its value
    in ISO 8601 format with second precision.
    """
    f_second = '%Y-%m-%dT%H:%M:%SZ'
    f_microsecond = '%Y-%m-%dT%H:%M:%S.%fZ'

    @classmethod
    def from_string(cls, s: str) -> 'Timestamp':
        """
        Initialise instance from string.

        Parameters
        ----------
        s
            timestamp string

        Returns
        -------
        Timestamp
            new timestamp
        """
        for f in (cls.f_second, cls.f_microsecond):
            try:
                return cls.strptime(s, f)
            except ValueError:
                pass
        else:
            raise ValueError(f'Date `{s}` does not match accepted formats!')

    def __str__(self):
        return self.strftime(self.f_second)


class JSONEncoder(json.JSONEncoder):
    """
    JSON Encoder capable of serialising enumerations and timestamps.
    """
    def default(self, o):
        """
        Serialise enumerations using their name.
        """
        if isinstance(o, Enum):
            return o.name
        elif isinstance(o, Timestamp):
            return str(o)
        else:
            return super().default(o)


@dataclass
class SerialisableDataclass:
    """
    Convenience methods for dataclasses.

    Convert dataclasses to JSON strings recursively using `str`.
    """
    def asdict(self) -> dict:
        """
        Dictionary representation of the dataclass and its members.

        Returns
        -------
        dict
            dataclass and its members as a dictionary
        """
        return asdict(self)

    def pprint(self, **pprint_kwargs) -> None:
        """
        Pretty print the dictionary representation of the dataclass.

        Parameters
        ----------
        pprint_kwargs
            additional keyword arguments for pprint.pprint
        """
        pprint(self.asdict(), **pprint_kwargs)

    def __str__(self):
        return JSONEncoder().encode(self.asdict())


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
