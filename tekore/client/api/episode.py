from tekore.client.process import single, model_list
from tekore.client.chunked import chunked, join_lists
from tekore.client.decor import send_and_process
from tekore.client.base import SpotifyBase
from tekore.model import FullEpisode, ModelList


class SpotifyEpisode(SpotifyBase):
    @send_and_process(single(FullEpisode))
    def episode(
            self,
            episode_id: str,
            market: str = None
    ) -> FullEpisode:
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

        Returns
        -------
        FullEpisode
            episode object
        """
        return self._get('episodes/' + episode_id, market=market)

    @chunked('episode_ids', 1, 50, join_lists)
    @send_and_process(model_list(FullEpisode, 'episodes'))
    def episodes(
            self,
            episode_ids: list,
            market: str = None
    ) -> ModelList:
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

        Returns
        -------
        ModelList
            list of episode objects
        """
        return self._get('episodes/?ids=' + ','.join(episode_ids), market=market)
