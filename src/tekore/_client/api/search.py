from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore.model import (
    FullArtistOffsetPaging,
    FullTrackPaging,
    SimpleAlbumPaging,
    SimpleAudiobookPaging,
    SimpleEpisodePaging,
    SimplePlaylistPaging,
    SimpleShowPaging,
)

paging_type = {
    "artists": FullArtistOffsetPaging,
    "albums": SimpleAlbumPaging,
    "audiobooks": SimpleAudiobookPaging,
    "episodes": SimpleEpisodePaging,
    "playlists": SimplePlaylistPaging,
    "shows": SimpleShowPaging,
    "tracks": FullTrackPaging,
}


def search_result(json: dict):
    """Unpack search result dicts into respective paging type constructors."""
    return tuple(paging_type[key](**json[key]) for key in json)


class SpotifySearch(SpotifyBase):
    """Search API endpoints."""

    @scopes()
    @send_and_process(search_result)
    @maximise_limit(50)
    def search(
        self,
        query: str,
        types: tuple = ("track",),
        market: str | None = None,
        include_external: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple:
        """
        Search for an item.

        Returns :class:`NotFound` if limit+offset would be above 1000.

        Parameters
        ----------
        query
            search query
        types
            resources to search for, tuple of strings containing
            artist, album, audiobook, track, playlist, show and/or episode
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        include_external
            if 'audio', response will include any externally hosted audio

        Returns
        -------
        tuple
            Paging objects containing the types of items searched for
            in the order that they were specified in 'types'.

            * artist: :class:`FullArtistOffsetPaging <model.FullArtistOffsetPaging>`
            * album: :class:`SimpleAlbumPaging <model.SimpleAlbumPaging>`
            * audiobook: :class:`SimpleAudiobookPaging <model.SimpleAudiobookPaging>`
            * episode: :class:`SimpleEpisodePaging <model.SimpleEpisodePaging>`
            * playlist: :class:`SimplePlaylistPaging <model.SimplePlaylistPaging>`
            * show: :class:`SimpleShowPaging <model.SimpleShowPaging>`
            * track: :class:`FullTrackPaging <model.FullTrackPaging>`

        Examples
        --------
        .. code:: python

            tracks, = spotify.search('monty python')
            artists, = spotify.search('sheeran', types=('artist',))
            albums, tracks = spotify.search('piano', types=('album', 'track'))
            spotify.search('gold album:boba artist:abba', types=('track',))
            spotify.search('bob year:1980-2020', types=('show',))

        .. note::
            You can narrow down search results by specifying field filters
            (e.g. year range, genre).
            See the `Search for an Item
            <https://developer.spotify.com/documentation/web-api/reference/>`_
            page of the official documentation for more information.

        """
        return self._get(
            "search",
            q=query,
            type=",".join(types),
            market=market,
            include_external=include_external,
            limit=limit,
            offset=offset,
        )
