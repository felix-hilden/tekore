from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import FullAudiobook, SimpleChapterPaging


class SpotifyAudiobook(SpotifyBase):
    """Audiobook API endpoints."""

    @scopes()
    @send_and_process(single(FullAudiobook))
    def audiobook(self, audiobook_id: str, market: str | None = None) -> FullAudiobook:
        """
        Get information for an audiobook.

        Parameters
        ----------
        audiobook_id
            audiobook ID
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the show is considered unavailable.
        """
        return self._get("audiobooks/" + audiobook_id, market=market)

    @scopes()
    @chunked("audiobook_ids", 1, 50, join_lists)
    @send_and_process(model_list(FullAudiobook, "audiobooks"))
    def audiobooks(
        self, audiobook_ids: list[str], market: str | None = None
    ) -> list[FullAudiobook]:
        """
        Get information for multiple audiobooks.

        Parameters
        ----------
        audiobook_ids
            the audiobook IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the show is considered unavailable.
        """
        return self._get("audiobook", ids=",".join(audiobook_ids), market=market)

    @scopes()
    @send_and_process(single(SimpleChapterPaging))
    @maximise_limit(50)
    def audiobook_chapters(
        self,
        audiobook_id: str,
        market: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> SimpleChapterPaging:
        """
        Get chapters of an audiobook.

        Parameters
        ----------
        audiobook_id
            audiobook ID
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
            f"audiobooks/{audiobook_id}/chapters",
            market=market,
            limit=limit,
            offset=offset,
        )
