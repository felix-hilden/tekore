from typing import Union

from spotipy.client.base import SpotifyBase
from spotipy.serialise import ModelList
from spotipy.model import FullArtist, SimpleAlbumPaging, FullTrack


class SpotifyArtist(SpotifyBase):
    def artist(self, artist_id: str) -> FullArtist:
        """
        Get information for an artist.

        Parameters
        ----------
        artist_id
            artist ID

        Returns
        -------
        FullArtist
            full artist object
        """
        json = self._get('artists/' + artist_id)
        return FullArtist(**json)

    def artists(self, artist_ids: list) -> ModelList:
        """
        Get information for multiple artists.

        Parameters
        ----------
        artist_ids
            list of artist IDs

        Returns
        -------
        ModelList
            list of full artist objects
        """
        json = self._get('artists/?ids=' + ','.join(artist_ids))
        return ModelList(FullArtist(**a) for a in json['artists'])

    def artist_albums(
            self,
            artist_id: str,
            include_groups: list = None,
            market: Union[str, None] = 'from_token',
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
            'album', 'single', 'appears_on', 'compilation'
        market
            None, an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimpleAlbumPaging
            paging containing simple album objects
        """
        json = self._get(
            f'artists/{artist_id}/albums',
            include_groups=include_groups,
            market=market,
            limit=limit,
            offset=offset
        )
        return SimpleAlbumPaging(**json)

    def artist_top_tracks(
            self,
            artist_id: str,
            country: str = 'from_token'
    ) -> ModelList:
        """
        Get an artist's top 10 tracks by country.

        Parameters
        ----------
        artist_id
            the artist ID
        country
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        ModelList
            list of full track objects
        """
        json = self._get(f'artists/{artist_id}/top-tracks', country=country)
        return ModelList(FullTrack(**t) for t in json['tracks'])

    def artist_related_artists(self, artist_id: str) -> ModelList:
        """
        Get artists similar to an identified artist.

        Similarity is based on analysis of
        the Spotify community's listening history.

        Parameters
        ----------
        artist_id
            artist ID

        Returns
        -------
        ModelList
            list of full artist objects
        """
        json = self._get(f'artists/{artist_id}/related-artists')
        return ModelList(FullArtist(**a) for a in json['artists'])
