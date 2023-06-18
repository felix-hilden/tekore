from datetime import datetime
from typing import List

from ..paging import OffsetPaging
from ..serialise import Model
from ..show.base import Show


class SimpleShow(Show):
    """
    Simplified show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """


class SimpleShowPaging(OffsetPaging):
    """Paging of simplified shows."""

    items: List[SimpleShow]


class SavedShow(Model):
    """Show saved in library."""

    added_at: datetime
    show: SimpleShow


class SavedShowPaging(OffsetPaging):
    """Paging of shows in library."""

    items: List[SavedShow]
