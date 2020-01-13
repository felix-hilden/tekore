from typing import Generator
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
        if page.next is not None:
            next_set = self._get_paging_result(page.next)
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
        if page.previous is not None:
            previous_set = self._get_paging_result(page.previous)
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
        yield page
        while page.next is not None:
            page = self.next(page)
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
        for p in self.all_pages(page):
            yield from p.items
