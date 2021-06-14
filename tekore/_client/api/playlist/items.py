from typing import List, Tuple

from tekore._auth import scope
from ...base import SpotifyBase
from ...decor import send_and_process, scopes
from ...process import top_item, nothing
from ...chunked import chunked, return_last


class SpotifyPlaylistItems(SpotifyBase):
    """Playlist API endpoints for manipulating playlist items."""

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @chunked('uris', 2, 100, return_last, reverse='position', reverse_pos=3)
    @send_and_process(top_item('snapshot_id'))
    def playlist_add(
            self,
            playlist_id: str,
            uris: list,
            position: int = None
    ) -> str:
        """
        Add items.

        Parameters
        ----------
        playlist_id
            playlist ID
        uris
            list of URIs, max 100 without chunking
        position
            index to insert the items in

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        return self._post(
            f'playlists/{playlist_id}/tracks',
            payload={'uris': uris},
            position=position
        )

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
    def playlist_clear(self, playlist_id: str) -> None:
        """
        Remove all items.

        Parameters
        ----------
        playlist_id
            playlist ID
        """
        return self._put(f'playlists/{playlist_id}/tracks', payload={'uris': []})

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
    def playlist_replace(self, playlist_id: str, uris: list) -> None:
        """
        Replace all items.

        Parameters
        ----------
        playlist_id
            playlist ID
        uris
            list of URIs, max 100
        """
        return self._put(
            f'playlists/{playlist_id}/tracks',
            payload={'uris': uris}
        )

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(top_item('snapshot_id'))
    def playlist_reorder(
            self,
            playlist_id: str,
            range_start: int,
            insert_before: int,
            range_length: int = 1,
            snapshot_id: str = None
    ) -> str:
        """
        Reorder items.

        Parameters
        ----------
        playlist_id
            playlist ID
        range_start
            position of the first item to be reordered
        range_length
            number of items to be reordered
        insert_before
            position where the items should be inserted
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        payload = {
            'range_start': range_start,
            'range_length': range_length,
            'insert_before': insert_before
        }
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._put(f'playlists/{playlist_id}/tracks', payload=payload)

    def _generic_playlist_remove(
            self,
            playlist_id: str,
            payload: dict,
            snapshot_id: str = None
    ) -> str:
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._delete(f'playlists/{playlist_id}/tracks', payload=payload)

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @chunked('uris', 2, 100, return_last, chain='snapshot_id', chain_pos=3)
    @send_and_process(top_item('snapshot_id'))
    def playlist_remove(
            self,
            playlist_id: str,
            uris: list,
            snapshot_id: str = None
    ) -> str:
        """
        Remove items by URI.

        Removes all occurrences of the specified items.
        Note that when chunked, ``snapshot_id`` is not updated between requests.

        Parameters
        ----------
        playlist_id
            playlist ID
        uris
            list of URIs, max 100 without chunking
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        items = [{'uri': uri} for uri in uris]
        return self._generic_playlist_remove(
            playlist_id,
            {'tracks': items},
            snapshot_id
        )

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(top_item('snapshot_id'))
    def playlist_remove_occurrences(
            self,
            playlist_id: str,
            refs: List[Tuple[str, int]],
            snapshot_id: str = None
    ) -> str:
        """
        Remove items by URI and position.

        Parameters
        ----------
        playlist_id
            playlist ID
        refs
            a list of tuples containing the URI and index of items to remove
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        gathered = {}
        for uri, ix in refs:
            gathered.setdefault(uri, []).append(ix)

        items = [
            {
                'uri': uri,
                'positions': ix_list
            }
            for uri, ix_list in gathered.items()
        ]
        return self._generic_playlist_remove(
            playlist_id,
            {'tracks': items},
            snapshot_id
        )

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(top_item('snapshot_id'))
    def playlist_remove_indices(
            self,
            playlist_id: str,
            indices: list,
            snapshot_id: str
    ) -> str:
        """
        Remove items by position.

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
        return self._generic_playlist_remove(
            playlist_id,
            {'positions': indices},
            snapshot_id
        )
