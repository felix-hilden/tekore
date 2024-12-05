from tekore._client.base import SpotifyBase
from tekore._client.decor import scopes, send_and_process
from tekore._client.process import top_item


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
