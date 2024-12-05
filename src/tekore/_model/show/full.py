from __future__ import annotations

from tekore._model.episode import SimpleEpisodePaging
from tekore._model.show import Show


class FullShow(Show):
    """
    Complete show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """

    episodes: SimpleEpisodePaging | None = None
