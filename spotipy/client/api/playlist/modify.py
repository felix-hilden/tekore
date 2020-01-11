from spotipy.client.base import SpotifyBase
from spotipy.model import FullPlaylist


class SpotifyPlaylistModify(SpotifyBase):
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
            'Content-Type': 'image/jpeg'
        }
        r = self._build_request(
            'PUT',
            f'playlists/{playlist_id}/images',
            headers
        )
        self._set_content(r, payload=image)
        self._send(r)

    def playlist_create(
            self,
            user_id: str,
            name: str,
            public: bool = True,
            description: str = ''
    ) -> FullPlaylist:
        """
        Create a playlist.

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

        Returns
        -------
        FullPlaylist
            created playlist
        """
        payload = {
            'name': name,
            'public': public,
            'description': description
        }
        json = self._post(f'users/{user_id}/playlists', payload=payload)
        return FullPlaylist(**json)

    def playlist_change_details(
            self,
            playlist_id: str,
            name: str = None,
            public: bool = None,
            collaborative: bool = None,
            description: str = None
    ) -> None:
        """
        Change a playlist's details.

        Requires the playlist-modify-public scope. To modify private playlists
        the playlist-modify-private scope is required.

        Parameters
        ----------
        playlist_id
            playlist ID
        name
            name of the playlist
        public
            is the playlist public
        collaborative
            is the playlist collaborative
        description
            description of the playlist
        """
        payload = {
            'name': name,
            'public': public,
            'collaborative': collaborative,
            'description': description,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        self._put('playlists/' + playlist_id, payload=payload)
