from tekore.client.base import SpotifyBase, SpotifyBaseAsync
from tekore.serialise import ModelList
from tekore.model import FullAlbum, SimpleTrackPaging


class SpotifyAlbum(SpotifyBase):
    def album(
            self,
            album_id: str,
            market: str = None
    ) -> FullAlbum:
        """
        Get an album.

        Parameters
        ----------
        album_id
            album ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        FullAlbum
            full album object
        """
        json = self._get('albums/' + album_id, market=market)
        return FullAlbum(**json)

    def album_tracks(
            self,
            album_id: str,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimpleTrackPaging:
        """
        Get tracks on album.

        Parameters
        ----------
        album_id
            album ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimpleTrackPaging
            paging containing simplified track objects
        """
        json = self._get(
            f'albums/{album_id}/tracks',
            market=market,
            limit=limit,
            offset=offset
        )
        return SimpleTrackPaging(**json)

    def albums(
            self,
            album_ids: list,
            market: str = None
    ) -> ModelList:
        """
        Get multiple albums.

        Parameters
        ----------
        album_ids
            list of album IDs (1..20)
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        ModelList
            list of full album objects
        """
        json = self._get('albums/?ids=' + ','.join(album_ids), market=market)
        return ModelList(FullAlbum(**a) for a in json['albums'])


class SpotifyAlbumAsync(SpotifyBaseAsync):
    async def album(
            self,
            album_id: str,
            market: str = None
    ) -> FullAlbum:
        """
        Get an album.

        Parameters
        ----------
        album_id
            album ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        FullAlbum
            full album object
        """
        json = await self._get('albums/' + album_id, market=market)
        return FullAlbum(**json)

    async def album_tracks(
            self,
            album_id: str,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimpleTrackPaging:
        """
        Get tracks on album.

        Parameters
        ----------
        album_id
            album ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimpleTrackPaging
            paging containing simplified track objects
        """
        json = await self._get(
            f'albums/{album_id}/tracks',
            market=market,
            limit=limit,
            offset=offset
        )
        return SimpleTrackPaging(**json)

    async def albums(
            self,
            album_ids: list,
            market: str = None
    ) -> ModelList:
        """
        Get multiple albums.

        Parameters
        ----------
        album_ids
            list of album IDs (1..20)
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        ModelList
            list of full album objects
        """
        json = await self._get('albums/?ids=' + ','.join(album_ids), market=market)
        return ModelList(FullAlbum(**a) for a in json['albums'])
