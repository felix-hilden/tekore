from spotipy.client.base import SpotifyBase
from spotipy.serialise import ModelList
from spotipy.convert import to_uri
from spotipy.model import (
    SimplePlaylistPaging,
    FullPlaylist,
    Image,
    PlaylistTrackPaging
)


class SpotifyPlaylist(SpotifyBase):
    def current_user_playlists(
            self,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by the current user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope
        to return collaborative playlists.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        json = self._get('me/playlists', limit=limit, offset=offset)
        return SimplePlaylistPaging(**json)

    def playlists(
            self,
            user_id: str,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by a user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope to return collaborative
        playlists. Collaborative playlists are only returned for current user.

        Parameters
        ----------
        user_id
            user ID
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        json = self._get(f'users/{user_id}/playlists', limit=limit, offset=offset)
        return SimplePlaylistPaging(**json)

    def playlist(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = 'from_token'
    ) -> FullPlaylist:
        """
        Get playlist of a user.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        FullPlaylist
            playlist object
        """
        json = self._get('playlists/' + playlist_id, fields=fields, market=market)
        return FullPlaylist(**json)

    def playlist_cover_image(self, playlist_id: str) -> ModelList:
        """
        Get cover image of a playlist. Note: returns a list of images.

        Returns
        -------
        ModelList
            list of cover images
        """
        json = self._get(f'playlists/{playlist_id}/images')
        return ModelList(Image(**i) for i in json)

    def playlist_cover_image_upload(self, playlist_id: str, image: str) -> None:
        """
        Upload a custom playlist cover image.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        image
            image data as a base64-encoded string
        """
        headers = {
            'Content-Type': 'image/jpg'
        }
        r = self._build_request(
            'PUT',
            f'playlists/{playlist_id}/images',
            headers
        )
        self._set_content(r, payload=image)
        self._send(r)

    def playlist_tracks(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = 'from_token',
            limit: int = 100,
            offset: int = 0
    ) -> PlaylistTrackPaging:
        """
        Get full details of the tracks of a playlist owned by a user.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return
        limit
            the number of items to return (1..100)
        offset
            the index of the first item to return
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        PlaylistTrackPaging
            paging object containing playlist tracks
        """
        json = self._get(
            f'playlists/{playlist_id}/tracks',
            limit=limit,
            offset=offset,
            fields=fields,
            market=market
        )
        return PlaylistTrackPaging(**json)

    def playlist_create(
            self,
            user_id: str,
            name: str,
            public: bool = True,
            description: str = ''
    ) -> None:
        """
        Create a playlist for a user.

        Requires the playlist-modify-public scope. To create a private playlist
        the playlist-modify-private scope is required.

        Parameters
        ----------
        user_id
            user ID
        name
            the name of the playlist
        public
            is the created playlist public
        description
            the description of the playlist
        """
        payload = {
            'name': name,
            'public': public,
            'description': description
        }
        self._post(f'users/{user_id}/playlists', payload=payload)

    def playlist_change_details(
            self,
            playlist_id: str,
            name: str = None,
            public: bool = None,
            collaborative: bool = None,
            description: str = None
    ) -> None:
        """
        Change a playlist's name and/or public/private state.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        name
            optional name of the playlist
        public
            optional is the playlist public
        collaborative
            optional is the playlist collaborative
        description
            optional description of the playlist
        """
        payload = {
            'name': name,
            'public': public,
            'collaborative': collaborative,
            'description': description,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        self._put('playlists/' + playlist_id, payload=payload)

    def playlist_tracks_add(
            self,
            playlist_id: str,
            track_ids: list,
            position: int = None
    ) -> None:
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
        """
        payload = {'uris': [to_uri('track', t) for t in track_ids]}
        self._post(
            f'playlists/{playlist_id}/tracks',
            payload=payload,
            position=position
        )

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
        payload = {'uris': [to_uri('track', t) for t in track_ids]}
        self._put(f'playlists/{playlist_id}/tracks)', payload=payload)

    def playlist_tracks_reorder(
            self,
            playlist_id: str,
            range_start: int,
            insert_before: int,
            range_length: int = 1,
            snapshot_id: str = None
    ) -> None:
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
            playlist's snapshot ID
        """
        payload = {
            'range_start': range_start,
            'range_length': range_length,
            'insert_before': insert_before
        }
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        self._put(f'playlists/{playlist_id}/tracks', payload=payload)

    def playlist_tracks_remove(
            self,
            playlist_id: str,
            track_ids: list,
            snapshot_id: str = None
    ) -> None:
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
            playlist's snapshot ID
        """
        tracks = [to_uri('track', t) for t in track_ids]
        payload = {'tracks': [{'uri': t} for t in tracks]}
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        self._delete(f'playlists/{playlist_id}/tracks', payload=payload)

    def playlist_tracks_remove_occurrences(
            self,
            playlist_id: str,
            track_refs: list,
            snapshot_id: str = None
    ) -> None:
        """
        Remove all occurrences of tracks from a playlist.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        track_refs
            an array of objects containing Spotify IDs of the
            tracks to remove with their current positions in the playlist.
            For example:
            >>> [{"id": "4iV5W9uYEdYUVa79Axb7Rh", "positions": [2]},
            ...  {"id": "1301WleyT98MSxVHPZCA6M", "positions": [7]}]
        snapshot_id
            id of the playlist snapshot
        """
        tracks = [
            {
                'uri': to_uri('track', tr['id']),
                'positions': tr['positions']
            }
            for tr in track_refs
        ]

        payload = {'tracks': tracks}
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        self._delete(f'playlists/{playlist_id}/tracks', payload=payload)
