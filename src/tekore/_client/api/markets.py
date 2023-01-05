from typing import List

from ..base import SpotifyBase
from ..decor import scopes, send_and_process
from ..process import top_item


class SpotifyMarkets(SpotifyBase):
    """Markets API endpoints."""

    @scopes()
    @send_and_process(top_item("markets"))
    def markets(self) -> List[str]:
        """
        Get available market country codes.

        Returns
        -------
        List[str]
            available markets
        """
        return self._get("markets")
