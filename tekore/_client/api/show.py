from ..base import SpotifyBase
from ..decor import send_and_process, maximise_limit, scopes
from ..process import single, model_list
from ..chunked import chunked, join_lists
from tekore._auth import scope
from tekore.model import FullShow, SimpleEpisodePaging, ModelList


class SpotifyShow(SpotifyBase):
    """Show API endpoints."""

    @scopes(optional=[scope.user_read_playback_position])
    @send_and_process(single(FullShow))
    def show(
            self,
            show_id: str,
            market: str = None
    ) -> FullShow:
        """
        Get information for a show.

        The user-read-playback-position scope allows
        episode resume points to be returned.

        Parameters
        ----------
        show_id
            show ID
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the show is considered unavailable.
        """
        return self._get('shows/' + show_id, market=market)

    @scopes(optional=[scope.user_read_playback_position])
    @chunked('show_ids', 1, 50, join_lists)
    @send_and_process(model_list(FullShow, 'shows'))
    def shows(
            self,
            show_ids: list,
            market: str = None
    ) -> ModelList[FullShow]:
        """
        Get information for multiple shows.

        The user-read-playback-position scope allows
        episode resume points to be returned.

        Parameters
        ----------
        show_ids
            the show IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the show is considered unavailable.
        """
        return self._get('shows/?ids=' + ','.join(show_ids), market=market)

    @scopes()
    @send_and_process(single(SimpleEpisodePaging))
    @maximise_limit(50)
    def show_episodes(
            self,
            show_id: str,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimpleEpisodePaging:
        """
        Get episodes of a show.

        Parameters
        ----------
        show_id
            show ID
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the show is considered unavailable.
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get(
            f'shows/{show_id}/episodes',
            market=market,
            limit=limit,
            offset=offset
        )
