from typing import List, Tuple

from tekore.client.process import top_item, nothing
from tekore.client.base import SpotifyBase, send_and_process
from tekore.convert import to_uri


class SpotifyPlaylistTracks(SpotifyBase):
    @send_and_process(top_item('snapshot_id'))
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
            list of track IDs
        position
            position to add the tracks

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        payload = {'uris': [to_uri('track', t) for t in track_ids]}
        return self._post(
            f'playlists/{playlist_id}/tracks',
            payload=payload,
            position=position
        )

    @send_and_process(nothing)
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
            list of track IDs to add to the playlist
        """
        track_uris = [to_uri('track', t) for t in track_ids]
        return self._put(f'playlists/{playlist_id}/tracks', payload={'uris': track_uris})

    @send_and_process(top_item('snapshot_id'))
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
        range_length
            the number of tracks to be reordered
        insert_before
            position where the tracks should be inserted
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

    def _generic_playlist_tracks_remove(
            self,
            playlist_id: str,
            payload: dict,
            snapshot_id: str = None
    ) -> str:
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._delete(f'playlists/{playlist_id}/tracks', payload=payload)

    @send_and_process(top_item('snapshot_id'))
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

        Parameters
        ----------
        playlist_id
            playlist ID
        track_ids
            list of track IDs
        snapshot_id
            snapshot ID for the playlist

        Returns
        -------
        str
            snapshot ID for the playlist
        """
        tracks = [{'uri': to_uri('track', t)} for t in track_ids]
        return self._generic_playlist_tracks_remove(
            playlist_id,
            {'tracks': tracks},
            snapshot_id
        )

    @send_and_process(top_item('snapshot_id'))
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
        gathered = {}
        for id_, ix in track_refs:
            gathered.setdefault(id_, []).append(ix)

        tracks = [
            {
                'uri': to_uri('track', id_),
                'positions': ix_list
            }
            for id_, ix_list in gathered.items()
        ]
        return self._generic_playlist_tracks_remove(
            playlist_id,
            {'tracks': tracks},
            snapshot_id
        )

    @send_and_process(top_item('snapshot_id'))
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
        return self._generic_playlist_tracks_remove(
            playlist_id,
            {'positions': indices},
            snapshot_id
        )
