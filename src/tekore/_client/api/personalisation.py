from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import single
from tekore.model import FullArtistOffsetPaging, FullTrackPaging


class SpotifyPersonalisation(SpotifyBase):
    """Personalisation API endpoints."""

    @scopes([scope.user_top_read])
    @send_and_process(single(FullArtistOffsetPaging))
    @maximise_limit(50)
    def current_user_top_artists(
        self, time_range: str = "medium_term", limit: int = 20, offset: int = 0
    ) -> FullArtistOffsetPaging:
        """
        Get the current user's top artists.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get(
            "me/top/artists", time_range=time_range, limit=limit, offset=offset
        )

    @scopes([scope.user_top_read])
    @send_and_process(single(FullTrackPaging))
    @maximise_limit(50)
    def current_user_top_tracks(
        self, time_range: str = "medium_term", limit: int = 20, offset: int = 0
    ) -> FullTrackPaging:
        """
        Get the current user's top tracks.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get(
            "me/top/tracks", time_range=time_range, limit=limit, offset=offset
        )
