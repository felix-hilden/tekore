from typing import Optional
from dataclasses import dataclass

from ..show import Show
from ..episode import SimpleEpisodePaging


@dataclass(repr=False)
class FullShow(Show):
    """
    Complete show object.

    :attr:`total_episodes` is undocumented by Spotify,
    so it might be missing or removed in a future version.
    """

    episodes: Optional[SimpleEpisodePaging] = None

    def __post_init__(self):
        super().__post_init__()
        if self.episodes is not None:
            self.episodes = SimpleEpisodePaging(**self.episodes)
