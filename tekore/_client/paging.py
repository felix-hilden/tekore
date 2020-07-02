from typing import Generator, Optional

from .base import SpotifyBase
from .decor import send_and_process
from tekore.model import Model, Paging, OffsetPaging
from tekore._error import NotFound


def parse_paging_result(result):
    """Parse through the varying paging layouts."""
    # If only one top-level key, the paging object is one level deeper
    if len(result) == 1:
        key = list(result.keys())[0]
        result = result[key]

    return result


class SpotifyPaging(SpotifyBase):
    """Paging navigation endpoints."""

    @send_and_process(parse_paging_result)
    def _get_paging_result(self, address: str):
        return self._get(address)

    def next(self, page: Paging) -> Optional[Paging]:
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
            return

        try:
            next_set = self._get_paging_result(page.next)
            return type(page)(**next_set)
        except NotFound:
            return

    async def _async_next(self, page: Paging) -> Optional[Paging]:
        if page.next is None:
            return

        try:
            next_set = await self._get_paging_result(page.next)
            return type(page)(**next_set)
        except NotFound:
            return

    def previous(self, page: OffsetPaging) -> Optional[OffsetPaging]:
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
            return

        previous_set = self._get_paging_result(page.previous)
        return type(page)(**previous_set)

    async def _async_previous(self, page: OffsetPaging) -> Optional[OffsetPaging]:
        if page.previous is None:
            return

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
        else:
            return self._sync_all_pages(page)

    def _sync_all_pages(self, page: Paging):
        while page is not None:
            yield page
            page = self.next(page)

    async def _async_all_pages(self, page: Paging):
        while page is not None:
            yield page
            page = await self._async_next(page)

    def all_items(
            self,
            page: Paging
    ) -> Generator[Model, None, None]:
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
        else:
            return self._sync_all_items(page)

    def _sync_all_items(self, page: Paging):
        for p in self.all_pages(page):
            yield from p.items

    async def _async_all_items(self, page: Paging):
        async for page in self._async_all_pages(page):
            for item in page.items:
                yield item
