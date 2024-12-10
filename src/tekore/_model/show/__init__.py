from datetime import datetime

from tekore._model.paging import OffsetPaging
from tekore._model.serialise import Model
from tekore._model.show.base import Show


class SimpleShow(Show):
    """
    Simplified show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """


class SimpleShowPaging(OffsetPaging):
    """Paging of simplified shows."""

    items: list[SimpleShow]


class SavedShow(Model):
    """Show saved in library."""

    added_at: datetime
    show: SimpleShow


class SavedShowPaging(OffsetPaging):
    """Paging of shows in library."""

    items: list[SavedShow]
