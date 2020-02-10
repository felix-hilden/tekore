from typing import Generator, Optional

from tekore.model.paging import Paging, OffsetPaging
from tekore.client.base import send_and_process, SpotifyBase
from tekore.serialise import SerialisableDataclass


def parse_paging_result(result):
    # If only one top-level key, the paging object is one level deeper
    if len(result) == 1:
        key = list(result.keys())[0]
        result = result[key]

    return result


class SpotifyPaging(SpotifyBase):
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
            paging object containing the next result set
        """
        if self.is_async:
            return self._async_next(page)

        if page.next is None:
            return

        next_set = self._get_paging_result(page.next)
        return type(page)(**next_set)

    async def _async_next(self, page: Paging) -> Optional[Paging]:
        if page.next is None:
            return

        next_set = await self._get_paging_result(page.next)
        return type(page)(**next_set)

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
            paging object containing the previous result set
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
        yield page
        while page.next is not None:
            page = self.next(page)
            yield page

    async def _async_all_pages(self, page: Paging):
        yield page
        while page.next is not None:
            page = await self._async_next(page)
            yield page

    def all_items(
            self,
            page: Paging
    ) -> Generator[SerialisableDataclass, None, None]:
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
