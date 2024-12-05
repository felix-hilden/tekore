from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists
from tekore._client.decor import scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import FullEpisode


class SpotifyEpisode(SpotifyBase):
    """Episode API endpoints."""

    @scopes()
    @send_and_process(single(FullEpisode))
    def episode(self, episode_id: str, market: str | None = None) -> FullEpisode:
        """
        Get information for an episode.

        Parameters
        ----------
        episode_id
            episode ID
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the episode is considered unavailable.
        """
        return self._get("episodes/" + episode_id, market=market)

    @scopes()
    @chunked("episode_ids", 1, 50, join_lists)
    @send_and_process(model_list(FullEpisode, "episodes"))
    def episodes(
        self, episode_ids: list[str], market: str | None = None
    ) -> list[FullEpisode]:
        """
        Get information for multiple episodes.

        Parameters
        ----------
        episode_ids
            the episode IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the episode is considered unavailable.
        """
        return self._get("episodes", ids=",".join(episode_ids), market=market)
