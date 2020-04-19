"""
Serialisation and convenience methods for :mod:`models <tekore.model>`.

The :class:`SerialisableDataclass` defined in this module along with other
supporting classes makes it possible to access dictionary and original
JSON representations of responses.

.. code:: python

    import tekore as tk

    # Call the Web API
    spotify = tk.Spotify(user_token)
    user = spotify.current_user()

    # Inspect the content
    print(repr(user))
    user.pprint()
    user.pprint(compact=True, depth=2)

    # Dictionary representation
    user.asdict()

    # Original JSON representation
    str(user)
"""

import json

from enum import Enum
from pprint import pprint
from datetime import datetime
from dataclasses import dataclass, asdict, fields


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
    JSON Encoder for :class:`SerialisableDataclass`.
    """
    def default(self, o):
        """
        Serialiser for individual members.

        Instances of :class:`Enum` and :class:`Timestamp` are serialised
        using their string representations.
        """
        if isinstance(o, (Enum, Timestamp)):
            return str(o)
        else:
            return super().default(o)


@dataclass(repr=False)
class SerialisableDataclass:
    """
    Convenience methods for dataclasses.

    Convert dataclasses to JSON strings recursively using ``str``.
    Note that calling ``str`` on the dataclass and its dictionary representation
    are not equivalent, because the former uses a :class:`JSONEncoder`.

    .. code:: python

        data = ...  # Dataclass
        s = str(data)
        d = data.asdict()

        str(d)  # Skips type conversions!
    """
    def asdict(self) -> dict:
        """
        Dictionary representation of the dataclass and its members.

        Note that no type conversions take place besides converting
        the dataclass hierarchy to dictionaries.

        Returns
        -------
        dict
            dataclass and its members as a dictionary
        """
        return asdict(self)

    def pprint(
            self,
            depth: int = None,
            compact: bool = False,
            **pprint_kwargs
    ) -> None:
        """
        Pretty print the dictionary representation of the dataclass.

        Parameters
        ----------
        depth
            number of levels printed
        compact
            combine items on the same line if they fit
        pprint_kwargs
            additional keyword arguments for pprint.pprint
        """
        pprint(self.asdict(), depth=depth, compact=compact, **pprint_kwargs)

    def __str__(self):
        return JSONEncoder().encode(self.asdict())

    @staticmethod
    def _member_repr(dataclass_type) -> str:
        v_fields = sorted(fields(dataclass_type), key=lambda f: f.name)
        joined = ', '.join(f.name for f in v_fields)
        return dataclass_type.__name__ + '(' + joined + ')'

    @staticmethod
    def _cut_by_comma(line: str, end: str, max_len: int) -> str:
        cut = line[:max_len - len(end)]
        mend = ','.join(cut.split(',')[:-1])
        return mend + end

    def __repr__(self):
        max_len = 75
        name = type(self).__name__
        lines = [f'{name} with fields:']

        for field in sorted(fields(self), key=lambda f: f.name):
            value = getattr(self, field.name)

            if isinstance(value, SerialisableDataclass):
                val_str = self._member_repr(type(value))
            elif isinstance(value, list):
                f_type = field.type.__args__[0]
                if issubclass(f_type, SerialisableDataclass):
                    f_str = self._member_repr(f_type)
                else:
                    f_str = f_type.__name__

                val_str = f'[{len(value)} x {f_str}]'
            elif isinstance(value, dict):
                v_fields = sorted(value.keys())
                f_str = ', '.join([f'"{f}"' for f in v_fields])
                val_str = f'{{{f_str}}}'
            elif isinstance(value, str):
                val_str = f'"{value}"'
            else:
                val_str = repr(value)

            line = f'  {field.name} = {val_str}'
            if len(line) > max_len:
                if isinstance(value, SerialisableDataclass):
                    line = self._cut_by_comma(line, ', ...)', max_len)
                elif isinstance(value, list) and '(' in line:
                    line = self._cut_by_comma(line, ', ...)]', max_len)
                elif isinstance(value, dict):
                    line = self._cut_by_comma(line, ', ...}', max_len)
                elif isinstance(value, str):
                    line = line[:max_len - 4] + '..."'

            lines.append(line)
        return '\n'.join(lines)


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
