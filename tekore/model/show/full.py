from dataclasses import dataclass

from tekore.model.show import Show
from tekore.model.episode import SimpleEpisodePaging


@dataclass(repr=False)
class FullShow(Show):
    episodes: SimpleEpisodePaging = None

    def __post_init__(self):
        super().__post_init__()
        if self.episodes is not None:
            self.episodes = SimpleEpisodePaging(**self.episodes)
