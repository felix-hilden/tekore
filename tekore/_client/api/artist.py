from typing import List, Union

from ..base import SpotifyBase
from ..decor import send_and_process, maximise_limit, scopes
from ..process import single, model_list
from ..chunked import chunked, join_lists
from tekore.model import (
    FullArtist,
    SimpleAlbumPaging,
    FullTrack,
    AlbumGroup,
    ModelList,
)


class SpotifyArtist(SpotifyBase):
    """Artist API endpoints."""

    @scopes()
    @send_and_process(single(FullArtist))
    def artist(self, artist_id: str) -> FullArtist:
        """
        Get information for an artist.

        Parameters
        ----------
        artist_id
            artist ID
        """
        return self._get('artists/' + artist_id)

    @scopes()
    @chunked('artist_ids', 1, 50, join_lists)
    @send_and_process(model_list(FullArtist, 'artists'))
    def artists(self, artist_ids: list) -> ModelList[FullArtist]:
        """
        Get information for multiple artists.

        Parameters
        ----------
        artist_ids
            list of artist IDs, max 50 without chunking
        """
        return self._get('artists/?ids=' + ','.join(artist_ids))

    @scopes()
    @send_and_process(single(SimpleAlbumPaging))
    @maximise_limit(50)
    def artist_albums(
            self,
            artist_id: str,
            include_groups: List[Union[str, AlbumGroup]] = None,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimpleAlbumPaging:
        """
        Get an artist's albums.

        Parameters
        ----------
        artist_id
            the artist ID
        include_groups
            album groups to include in the response
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        if include_groups is not None:
            include_groups = ','.join(str(g) for g in include_groups)
        return self._get(
            f'artists/{artist_id}/albums',
            include_groups=include_groups,
            market=market,
            limit=limit,
            offset=offset
        )

    @scopes()
    @send_and_process(model_list(FullTrack, 'tracks'))
    def artist_top_tracks(
            self,
            artist_id: str,
            market: str
    ) -> ModelList[FullTrack]:
        """
        Get an artist's top 10 tracks by country.

        Parameters
        ----------
        artist_id
            the artist ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get(f'artists/{artist_id}/top-tracks', country=market)

    @scopes()
    @send_and_process(model_list(FullArtist, 'artists'))
    def artist_related_artists(self, artist_id: str) -> ModelList[FullArtist]:
        """
        Get artists similar to an identified artist.

        Similarity is based on analysis of
        the Spotify community's listening history.

        Parameters
        ----------
        artist_id
            artist ID
        """
        return self._get(f'artists/{artist_id}/related-artists')
