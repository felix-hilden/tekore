from ...base import SpotifyBase
from ...decor import send_and_process, scopes
from ...process import single, nothing
from tekore._auth import scope
from tekore._sender import Request
from tekore.model import FullPlaylist


class SpotifyPlaylistModify(SpotifyBase):
    """Playlist API endpoints for modifying playlists."""

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
    def playlist_cover_image_upload(self, playlist_id: str, image: str) -> None:
        """
        Upload a custom playlist cover image.

        Parameters
        ----------
        playlist_id
            playlist ID
        image
            image data as a base64-encoded string
        """
        return Request(
            method='PUT',
            url=f'playlists/{playlist_id}/images',
            headers={'Content-Type': 'image/jpeg'},
            content=image,
        ), ()

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(single(FullPlaylist))
    def playlist_create(
            self,
            user_id: str,
            name: str,
            public: bool = True,
            description: str = ''
    ) -> FullPlaylist:
        """
        Create a playlist.

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
        return self._post(f'users/{user_id}/playlists', payload=payload)

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
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
        return self._put('playlists/' + playlist_id, payload=payload)
