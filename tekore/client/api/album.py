from tekore.client.process import single, model_list
from tekore.client.base import SpotifyBase, send_and_process
from tekore.serialise import ModelList
from tekore.model import FullAlbum, SimpleTrackPaging


class SpotifyAlbum(SpotifyBase):
    @send_and_process(single(FullAlbum))
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
        return self._get('albums/' + album_id, market=market)

    @send_and_process(single(SimpleTrackPaging))
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
        return self._get(
            f'albums/{album_id}/tracks',
            market=market,
            limit=limit,
            offset=offset
        )

    @send_and_process(model_list(FullAlbum, 'albums'))
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
        return self._get('albums/?ids=' + ','.join(album_ids), market=market)
