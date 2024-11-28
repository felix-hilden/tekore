from ..base import SpotifyBase
from ..decor import scopes, send_and_process
from ..process import top_item


class SpotifyMarkets(SpotifyBase):
    """Markets API endpoints."""

    @scopes()
    @send_and_process(top_item("markets"))
    def markets(self) -> list[str]:
        """
        Get available market country codes.

        Returns
        -------
        list[str]
            available markets
        """
        return self._get("markets")
