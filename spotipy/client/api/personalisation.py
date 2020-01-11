from spotipy.model import FullArtistOffsetPaging, FullTrackPaging
from spotipy.client.base import SpotifyBase


class SpotifyPersonalisation(SpotifyBase):
    def current_user_top_artists(
            self,
            time_range: str = 'medium_term',
            limit: int = 20,
            offset: int = 0
    ) -> FullArtistOffsetPaging:
        """
        Get the current user's top artists.

        Requires the user-top-read scope.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        FullArtistOffsetPaging
            paging object containing artists
        """
        json = self._get(
            'me/top/artists',
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        return FullArtistOffsetPaging(**json)

    def current_user_top_tracks(
            self,
            time_range: str = 'medium_term',
            limit: int = 20,
            offset: int = 0
    ) -> FullTrackPaging:
        """
        Get the current user's top tracks.

        Requires the user-top-read scope.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        FullTrackPaging
            paging object containing full tracks
        """
        json = self._get(
            'me/top/tracks',
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        return FullTrackPaging(**json)
