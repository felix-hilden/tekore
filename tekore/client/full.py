from typing import Generator, AsyncGenerator
from contextlib import contextmanager

from tekore.model.paging import Paging, OffsetPaging
from tekore.serialise import SerialisableDataclass

from tekore.client.api import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyTrack,
    SpotifyUser,
)


class Spotify(
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyTrack,
    SpotifyUser,
):
    @contextmanager
    def token_as(self, token) -> 'Spotify':
        """
        Temporarily use a different token with requests.

        Parameters
        ----------
        token
            access token

        Returns
        -------
        Spotify
            self


        """
        self.token, old_token = token, self.token
        yield self
        self.token = old_token

    def next(self, page: Paging) -> Paging:
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
        # If async sender - return Awaitable
        if self.is_async:
            return self.__next_async(page)

        if page.next is not None:
            next_set = self._get_paging_result(page.next)
            return type(page)(**next_set)

    async def __next_async(self, page: Paging) -> Paging:
        if page.next is not None:
            next_set = await self._get_paging_result(page.next)
            return type(page)(**next_set)

    def previous(self, page: OffsetPaging) -> OffsetPaging:
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
        # If async sender - return Awaitable
        if self.is_async:
            return self.__previous_async(page)

        if page.previous is not None:
            previous_set = self._get_paging_result(page.previous)
            return type(page)(**previous_set)

    async def __previous_async(self, page: OffsetPaging) -> OffsetPaging:
        if page.previous is not None:
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
        # If async sender - return Awaitable
        if self.is_async:
            return self.__all_pages_async(page)

        yield page
        while page.next is not None:
            page = self.next(page)
            yield page

    async def __all_pages_async(self, page: Paging) -> AsyncGenerator[Paging, None]:
        yield page
        while page.next is not None:
            page = await self.__next_async(page)
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
        # If async sender - return Awaitable
        if self.is_async:
            return self.__all_items_async(page)

        for p in self.all_pages(page):
            yield from p.items

    async def __all_items_async(
            self,
            page: Paging
    ) -> AsyncGenerator[SerialisableDataclass, None]:
        async for p in await self.all_pages(page):
            for item in p.items:
                yield item
