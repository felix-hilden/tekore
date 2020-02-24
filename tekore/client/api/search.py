from tekore.client.decor import send_and_process, maximise_limit
from tekore.client.base import SpotifyBase
from tekore.model import (
    FullArtistOffsetPaging,
    FullTrackPaging,
    SimpleAlbumPaging,
    SimplePlaylistPaging,
)

paging_type = {
    'artist': FullArtistOffsetPaging,
    'album': SimpleAlbumPaging,
    'playlist': SimplePlaylistPaging,
    'track': FullTrackPaging,
}


def search_result(json: dict):
    """
    Unpack search result dicts into respective paging type constructors.
    """
    return tuple(paging_type[key[:-1]](**json[key]) for key in json.keys())


class SpotifySearch(SpotifyBase):
    @send_and_process(search_result)
    @maximise_limit(50)
    def search(
            self,
            query: str,
            types: tuple = ('track',),
            market: str = None,
            include_external: str = None,
            limit: int = 20,
            offset: int = 0
    ):
        """
        Search for an item.

        Requires the user-read-private scope.
        Returns 404 - Not Found if limit+offset would be above 2000.

        Parameters
        ----------
        query
            search query
        types
            resources to search for, tuple of strings containing
            artist, album, track and/or playlist
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
            paging objects containing the types of items searched for
            in the order that they were specified in 'types'

        Examples
        --------
        .. code:: python

            tracks, = spotify.search('monty python')
            artists, = spotify.search('sheeran', types=('artist',))
            albums, tracks = spotify.search('piano', types=('album', 'track'))
        """
        return self._get(
            'search',
            q=query,
            type=','.join(types),
            market=market,
            include_external=include_external,
            limit=limit,
            offset=offset
        )
