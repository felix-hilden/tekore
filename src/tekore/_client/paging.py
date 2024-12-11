from __future__ import annotations

from collections.abc import Generator

from tekore._sender import BadRequest
from tekore.model import Model, OffsetPaging, Paging

from .base import SpotifyBase
from .decor import send_and_process


def parse_paging_result(result: dict) -> dict:
    """Parse through the varying paging layouts."""
    # If only one top-level key, the paging object is one level deeper
    if len(result) == 1:
        key = next(iter(result.keys()))
        result = result[key]

    return result


class SpotifyPaging(SpotifyBase):
    """Paging navigation endpoints."""

    @send_and_process(parse_paging_result)
    def _get_paging_result(self, address: str):
        return self._get(address)

    def next(self, page: Paging) -> Paging | None:
        """
        Retrieve the next result set of a paging object.

        Parameters
        ----------
        page
            paging object

        Returns
        -------
        Paging
            next result set
        """
        if self.is_async:
            return self._async_next(page)

        if page.next is None:
            return None

        try:
            next_set = self._get_paging_result(page.next)
            return type(page)(**next_set)
        except BadRequest:
            return None

    async def _async_next(self, page: Paging) -> Paging | None:
        if page.next is None:
            return None

        try:
            next_set = await self._get_paging_result(page.next)
            return type(page)(**next_set)
        except BadRequest:
            return None

    def previous(self, page: OffsetPaging) -> OffsetPaging | None:
        """
        Retrieve the previous result set of a paging object.

        Parameters
        ----------
        page
            offset-based paging object

        Returns
        -------
        OffsetPaging
            previous result set
        """
        if self.is_async:
            return self._async_previous(page)

        if page.previous is None:
            return None

        previous_set = self._get_paging_result(page.previous)
        return type(page)(**previous_set)

    async def _async_previous(self, page: OffsetPaging) -> OffsetPaging | None:
        if page.previous is None:
            return None

        previous_set = await self._get_paging_result(page.previous)
        return type(page)(**previous_set)

    def all_pages(self, page: Paging) -> Generator[Paging, None, None]:
        """
        Retrieve all pages of a paging.

        Request and yield new (next) pages until the end of the paging.
        The paging that was given as an argument is yielded as the first result.

        Parameters
        ----------
        page
            paging object

        Returns
        -------
        Generator
            all pages within a paging
        """
        if self.is_async:
            return self._async_all_pages(page)
        return self._sync_all_pages(page)

    def _sync_all_pages(self, page: Paging):
        current: Paging | None = page
        while current is not None:
            yield current
            current = self.next(current)

    async def _async_all_pages(self, page: Paging):
        current: Paging | None = page
        while current is not None:
            yield current
            current = await self._async_next(current)

    def all_items(self, page: Paging) -> Generator[Model, None, None]:
        """
        Retrieve all items from all pages of a paging.

        Request and yield new (next) items until the end of the paging.
        The items in the paging that was given as an argument are yielded first.

        Parameters
        ----------
        page
            paging object

        Returns
        -------
        Generator
            all items within a paging
        """
        if self.is_async:
            return self._async_all_items(page)
        return self._sync_all_items(page)

    def _sync_all_items(self, paging: Paging):
        for page in self.all_pages(paging):
            yield from page.items

    async def _async_all_items(self, paging: Paging):
        async for page in self._async_all_pages(paging):
            for item in page.items:
                yield item
