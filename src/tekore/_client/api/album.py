from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import FullAlbum, SimpleTrackPaging


class SpotifyAlbum(SpotifyBase):
    """Album API endpoints."""

    @scopes()
    @send_and_process(single(FullAlbum))
    def album(self, album_id: str, market: str | None = None) -> FullAlbum:
        """
        Get an album.

        Parameters
        ----------
        album_id
            album ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get("albums/" + album_id, market=market)

    @scopes()
    @send_and_process(single(SimpleTrackPaging))
    @maximise_limit(50)
    def album_tracks(
        self, album_id: str, market: str | None = None, limit: int = 20, offset: int = 0
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
        """
        return self._get(
            f"albums/{album_id}/tracks", market=market, limit=limit, offset=offset
        )

    @scopes()
    @chunked("album_ids", 1, 20, join_lists)
    @send_and_process(model_list(FullAlbum, "albums"))
    def albums(
        self, album_ids: list[str], market: str | None = None
    ) -> list[FullAlbum]:
        """
        Get multiple albums.

        Parameters
        ----------
        album_ids
            list of album IDs, max 20 without chunking
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get("albums", ids=",".join(album_ids), market=market)
