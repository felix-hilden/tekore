from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists
from tekore._client.decor import scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import FullChapter


class SpotifyChapter(SpotifyBase):
    """Chapter API endpoints."""

    @scopes()
    @send_and_process(single(FullChapter))
    def chapter(self, chapter_id: str, market: str | None = None) -> FullChapter:
        """
        Get information for a chapter.

        Parameters
        ----------
        chapter_id
            chapter ID
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the episode is considered unavailable.
        """
        return self._get("chapters/" + chapter_id, market=market)

    @scopes()
    @chunked("chapter_ids", 1, 50, join_lists)
    @send_and_process(model_list(FullChapter, "chapters"))
    def chapters(
        self, chapter_ids: list[str], market: str | None = None
    ) -> list[FullChapter]:
        """
        Get information for multiple chapters.

        Parameters
        ----------
        chapter_ids
            the chapter IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code.
            If a user token is used to authenticate, the country associated
            with it overrides this parameter.
            If an application token is used and no market is specified,
            the episode is considered unavailable.
        """
        return self._get("chapters", ids=",".join(chapter_ids), market=market)
