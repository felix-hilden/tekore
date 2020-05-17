from typing import List, Tuple, Union

from ...decor import deprecated
from .items import SpotifyPlaylistItems
from .modify import SpotifyPlaylistModify
from .view import SpotifyPlaylistView

from tekore._convert import to_uri
from tekore.model import PlaylistTrackPaging


class SpotifyPlaylist(
    SpotifyPlaylistView,
    SpotifyPlaylistModify,
    SpotifyPlaylistItems,
):
    @deprecated('2.0', '3.0', 'playlist_items')
    def playlist_tracks(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = None,
            episodes_as_tracks: bool = False,
            limit: int = 100,
            offset: int = 0
    ) -> Union[PlaylistTrackPaging, dict]:
        """
        Get full details of the tracks of a playlist owned by a user.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return, see the Web API documentation for details
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
            when using a user token to authenticate.
            For episodes in the playlist, if a user token is used,
            the country associated with it overrides this parameter.
            If an application token is used and no market is specified,
            episodes are considered unavailable and returned as None.
        episodes_as_tracks
            if True, return episodes with track-like fields
        limit
            the number of items to return (1..100)
        offset
            the index of the first item to return

        Returns
        -------
        Union[PlaylistTrackPaging, dict]
            paging object containing playlist tracks, or raw dictionary
            if ``fields`` or ``episodes_as_tracks`` was specified
        """
        return self.playlist_items(
            playlist_id,
            fields,
            market,
            episodes_as_tracks,
            limit,
            offset,
        )

    @deprecated('2.0', '3.0', 'playlist_add')
    def playlist_tracks_add(
            self,
            playlist_id: str,
            track_ids: list,
            position: int = None
    ) -> str:
        """
        Add tracks to a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        track_ids
            list of track IDs, max 100 without chunking
        position
            position to add the tracks

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        uris = [to_uri('track', t) for t in track_ids]
        return self.playlist_add(
            playlist_id,
            uris,
            position
        )

    @deprecated('2.0', '3.0', 'playlist_clear')
    def playlist_tracks_clear(self, playlist_id: str) -> None:
        """
        Remove all tracks in a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        """
        return self.playlist_clear(playlist_id)

    @deprecated('2.0', '3.0', 'playlist_replace')
    def playlist_tracks_replace(self, playlist_id: str, track_ids: list) -> None:
        """
        Replace all tracks in a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        track_ids
            list of track IDs, max 100
        """
        uris = [to_uri('track', t) for t in track_ids]
        return self.playlist_replace(playlist_id, uris)

    @deprecated('2.0', '3.0', 'playlist_reorder')
    def playlist_tracks_reorder(
            self,
            playlist_id: str,
            range_start: int,
            insert_before: int,
            range_length: int = 1,
            snapshot_id: str = None
    ) -> str:
        """
        Reorder tracks in a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        range_start
            position of the first track to be reordered
        insert_before
            position where the tracks should be inserted
        range_length
            the number of tracks to be reordered
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        return self.playlist_reorder(
            playlist_id,
            range_start,
            insert_before,
            range_length,
            snapshot_id,
        )

    @deprecated('2.0', '3.0', 'playlist_remove')
    def playlist_tracks_remove(
            self,
            playlist_id: str,
            track_ids: list,
            snapshot_id: str = None
    ) -> str:
        """
        Remove all occurrences of tracks from a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Note that when chunked, ``snapshot_id`` is not updated between requests.

        Parameters
        ----------
        playlist_id
            playlist ID
        track_ids
            list of track IDs, max 100 without chunking
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        uris = [to_uri('track', t) for t in track_ids]
        return self.playlist_remove(playlist_id, uris, snapshot_id)

    @deprecated('2.0', '3.0', 'playlist_remove_occurrences')
    def playlist_tracks_remove_occurrences(
            self,
            playlist_id: str,
            track_refs: List[Tuple[str, int]],
            snapshot_id: str = None
    ) -> str:
        """
        Remove tracks from a playlist by track ID and position.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        track_refs
            a list of tuples containing the ID and index of tracks to remove
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        refs = [(to_uri('track', id_), ix) for id_, ix in track_refs]
        return self.playlist_remove_occurrences(playlist_id, refs, snapshot_id)

    @deprecated('2.0', '3.0', 'playlist_remove_indices')
    def playlist_tracks_remove_indices(
            self,
            playlist_id: str,
            indices: list,
            snapshot_id: str
    ) -> str:
        """
        Remove tracks from a playlist by position.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        indices
            a list of indices of tracks to remove
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        return self.playlist_remove_indices(playlist_id, indices, snapshot_id)
