from enum import Enum, EnumMeta
from warnings import warn

from pydantic import BaseModel


class StrEnumMeta(EnumMeta):
    """
    Metaclass for StrEnum that provides case-insensitive get.

    This does not change values.
    """

    def __new__(mcs, cls, bases, classdict, **kwds):  # noqa: N804
        """Override `__new__` to make all keys lowercase."""
        enum_class = super().__new__(mcs, cls, bases, classdict, **kwds)
        copied_member_map = dict(enum_class._member_map_)
        enum_class._member_map_.clear()
        for k, v in copied_member_map.items():
            enum_class._member_map_[k.lower()] = v
        return enum_class

    def __getitem__(cls, name: str):
        # Ignore case on get item
        return super().__getitem__(name.lower())


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    """
    Convert enumeration members to strings using their name.

    Ignores case when getting items. This does not change values.
    """

    @classmethod
    def _missing_(cls, value):
        return cls[value.lower()]

    def __str__(self) -> str:
        return self.name


class Model(BaseModel):
    """Response model base."""

    def __init__(self, **data) -> None:
        """"""  # noqa: D419
        super().__init__(**data)
        unknowns = set(data.keys()) - set(self.__dict__.keys())
        cls_name = self.__class__.__name__
        for arg in unknowns:
            msg = (
                f"{cls_name} contains unknown attribute: `{arg}`, which was discarded."
                " This warning may be safely ignored. Please consider upgrading Tekore."
            )
            warn(msg, UnknownModelAttributeWarning, stacklevel=5)


class UnknownModelAttributeWarning(RuntimeWarning):
    """The response model contains an unknown attribute."""
