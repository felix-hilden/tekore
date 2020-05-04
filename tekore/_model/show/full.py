from dataclasses import dataclass

from ..show import Show
from ..episode import SimpleEpisodePaging


@dataclass(repr=False)
class FullShow(Show):
    """
    Complete show object.
    """
    episodes: SimpleEpisodePaging = None

    def __post_init__(self):
        super().__post_init__()
        if self.episodes is not None:
            self.episodes = SimpleEpisodePaging(**self.episodes)
