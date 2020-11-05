from typing import List, Optional
from dataclasses import dataclass

from ..paging import OffsetPaging
from ..show.base import Show
from ..serialise import Model, ModelList, Timestamp


@dataclass(repr=False)
class SimpleShow(Show):
    """
    Simplified show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """

    total_episodes: Optional[int] = None


@dataclass(repr=False)
class SimpleShowPaging(OffsetPaging):
    """Paging of simplified shows."""

    items: List[SimpleShow]

    def __post_init__(self):
        """
        Do some setup after initialisation.

        Args:
            self: (todo): write your description
        """
        self.items = ModelList(SimpleShow(**i) for i in self.items)


@dataclass(repr=False)
class SavedShow(Model):
    """Show saved in library."""

    added_at: Timestamp
    show: SimpleShow

    def __post_init__(self):
        """
        Do some setup after initialisation.

        Args:
            self: (todo): write your description
        """
        self.added_at = Timestamp.from_string(self.added_at)
        self.show = SimpleShow(**self.show)


@dataclass(repr=False)
class SavedShowPaging(OffsetPaging):
    """Paging of shows in library."""

    items: List[SavedShow]

    def __post_init__(self):
        """
        Do some setup after initialisation.

        Args:
            self: (todo): write your description
        """
        self.items = ModelList(SavedShow(**i) for i in self.items)
