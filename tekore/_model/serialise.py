import json

from enum import Enum
from typing import Union, TypeVar, List
from pprint import pprint
from warnings import warn
from datetime import datetime
from dataclasses import dataclass, asdict, fields


class StrEnum(str, Enum):
    """Convert enumeration members to strings using their name."""

    def __str__(self):
        return self.name


class Timestamp(datetime):
    """
    Timestamp from different precisions.

    String representation is the ISO 8601 format with second precision.
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
    """JSON Encoder for response models."""

    def default(self, o):
        """Convert into serialisable data types."""
        if isinstance(o, (Enum, Timestamp)):
            return str(o)
        elif isinstance(o, Model):
            return asdict(o)
        else:
            return super().default(o)


def member_repr(dataclass_type) -> str:
    """Construct representation of fields of type Model."""
    v_fields = sorted(fields(dataclass_type), key=lambda f: f.name)
    joined = ', '.join(f.name for f in v_fields)
    return dataclass_type.__name__ + '(' + joined + ')'


def cut_by_comma(line: str, end: str, max_len: int) -> str:
    """Cut line to the appropriate comma."""
    cut = line[:max_len - len(end)]
    mend = ','.join(cut.split(',')[:-1])
    return mend + end


def field_repr(field, value) -> str:
    """Construct field representations."""
    if isinstance(value, Model):
        text = member_repr(type(value))
    elif isinstance(value, list):
        outer_type = field.type
        if outer_type.__origin__ is Union:
            outer_type = outer_type.__args__[0]

        inner_type = outer_type.__args__[0]

        if issubclass(inner_type, Model):
            f_str = member_repr(inner_type)
        else:
            f_str = inner_type.__name__

        text = f'[{len(value)} x {f_str}]'
    elif isinstance(value, dict):
        v_fields = sorted(value.keys())
        f_str = ', '.join([f"'{f}'" for f in v_fields])
        text = f'{{{f_str}}}'
    elif isinstance(value, str):
        text = f"'{value}'"
    else:
        text = repr(value)

    return text


def trim_line(line: str, value, max_len: int = 75) -> str:
    """Trim line based on field type."""
    if len(line) > max_len:
        if isinstance(value, Model):
            line = cut_by_comma(line, ', ...)', max_len)
        elif isinstance(value, list) and '(' in line:
            line = cut_by_comma(line, ', ...)]', max_len)
        elif isinstance(value, dict):
            line = cut_by_comma(line, ', ...}', max_len)
        elif isinstance(value, str):
            line = line[:max_len - 4] + '...\''

    return line


class Serialisable:
    """Serialisation and convenience methods for response models."""

    def json(self) -> str:
        """
        JSON representation of a model.

        Returns
        -------
        str
            JSON representation
        """
        return JSONEncoder().encode(self)

    def asbuiltin(self) -> Union[dict, list]:
        """
        Builtin representation of a model as dictionaries and lists.

        Returns
        -------
        Union[dict, list]
            builtin representation
        """
        return json.loads(self.json())

    def pprint(
            self,
            depth: int = None,
            compact: bool = True,
            **pprint_kwargs
    ) -> None:
        """
        Pretty print the builtin representation of a model.

        Parameters
        ----------
        depth
            number of levels printed, all levels printed by default
        compact
            combine items on the same line if they fit
        pprint_kwargs
            additional keyword arguments for ``pprint.pprint``
        """
        pprint(self.asbuiltin(), depth=depth, compact=compact, **pprint_kwargs)


class UnknownModelAttributeWarning(RuntimeWarning):
    """The response model contains an unknown attribute."""


@dataclass(repr=False)
class Model(Serialisable):
    """Dataclass that provides a readable ``repr`` of its fields."""

    def __repr__(self):
        name = type(self).__name__
        lines = [f'{name} with fields:']

        for field in sorted(fields(self), key=lambda f: f.name):
            value = getattr(self, field.name)
            text = field_repr(field, value)
            line = trim_line(f'  {field.name} = {text}', value)
            lines.append(line)

        return '\n'.join(lines)

    @classmethod
    def from_kwargs(cls, kwargs):
        """Create the Model and patch unknown kwargs in."""
        # Adapted from Stack Overflow: https://stackoverflow.com/a/55101438/7089239
        cls_fields = {field.name for field in fields(cls)}

        # split into known and unknown kwargs
        known_kwargs, unknown_kwargs = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                known_kwargs[name] = val
            else:
                unknown_kwargs[name] = val

        model = cls(**known_kwargs)

        for name, val in unknown_kwargs.items():
            setattr(model, name, val)
            msg = (
                f'\nResponse contains unknown attribute: `{name}`\n'
                'This warning may be safely ignored. Please consider upgrading Tekore.'
            )
            warn(msg, UnknownModelAttributeWarning, stacklevel=5)
        return model


T = TypeVar('T')


class ModelList(List[T], Serialisable):
    """List that provides a readable ``repr`` of its items."""

    def __repr__(self):
        name = type(self).__name__
        lines = [f'{name} with items: [']

        for model in self:
            # Hack: can leave field out because nested lists don't exist
            text = field_repr(None, model)
            line = trim_line(f'  {text}', model)
            lines.append(line)

        return '\n'.join(lines + [']'])
