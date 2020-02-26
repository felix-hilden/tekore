from typing import List

from tekore.client.process import single, nothing
from tekore.client.chunked import chunked, join_lists, return_none
from tekore.client.decor import send_and_process, maximise_limit
from tekore.client.base import SpotifyBase
from tekore.model import SavedAlbumPaging, SavedTrackPaging


class SpotifyLibrary(SpotifyBase):
    @send_and_process(single(SavedAlbumPaging))
    @maximise_limit(50)
    def saved_albums(
            self,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SavedAlbumPaging:
        """
        Get a list of the albums saved in the current user's Your Music library.

        Requires the user-library-read scope.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SavedAlbumPaging
            paging object containing saved albums
        """
        return self._get('me/albums', market=market, limit=limit, offset=offset)

    @chunked('album_ids', 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_albums_contains(self, album_ids: list) -> List[bool]:
        """
        Check if user has saved albums.

        Requires the user-library-read scope.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking

        Returns
        -------
        list
            list of booleans in the same order the album IDs were given
        """
        return self._get('me/albums/contains?ids=' + ','.join(album_ids))

    @chunked('album_ids', 1, 50, return_none)
    @send_and_process(nothing)
    def saved_albums_add(self, album_ids: list) -> None:
        """
        Save albums for current user.

        Requires the user-library-modify scope.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking
        """
        return self._put('me/albums?ids=' + ','.join(album_ids))

    @chunked('album_ids', 1, 50, return_none)
    @send_and_process(nothing)
    def saved_albums_delete(self, album_ids: list) -> None:
        """
        Remove albums for current user.

        Requires the user-library-modify scope.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking
        """
        return self._delete('me/albums?ids=' + ','.join(album_ids))

    @send_and_process(single(SavedTrackPaging))
    @maximise_limit(50)
    def saved_tracks(
            self,
            market: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SavedTrackPaging:
        """
        Get a list of the songs saved in the current user's Your Music library.

        Requires the user-library-read scope.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SavedTrackPaging
            paging object containing saved tracks
        """
        return self._get('me/tracks', market=market, limit=limit, offset=offset)

    @chunked('track_ids', 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_tracks_contains(self, track_ids: list) -> List[bool]:
        """
        Check if user has saved tracks.

        Requires the user-library-read scope.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking

        Returns
        -------
        list
            list of booleans in the same order the track IDs were given
        """
        return self._get('me/tracks/contains?ids=' + ','.join(track_ids))

    @chunked('track_ids', 1, 50, return_none)
    @send_and_process(nothing)
    def saved_tracks_add(self, track_ids: list) -> None:
        """
        Save tracks for current user.

        Requires the user-library-modify scope.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking
        """
        return self._put('me/tracks/?ids=' + ','.join(track_ids))

    @chunked('track_ids', 1, 50, return_none)
    @send_and_process(nothing)
    def saved_tracks_delete(self, track_ids: list) -> None:
        """
        Remove tracks for current user.

        Requires the user-library-modify scope.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking
        """
        return self._delete('me/tracks/?ids=' + ','.join(track_ids))
