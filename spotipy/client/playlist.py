from spotipy.client.base import SpotifyBase
from spotipy.convert import to_uri


class SpotifyPlaylist(SpotifyBase):
    def current_user_playlists(self, limit: int = 20, offset: int = 0):
        """
        Get a list of the playlists owned or followed by the current user.

        Parameters:
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('me/playlists', limit=limit, offset=offset)

    def playlists(self, user_id: str, limit: int = 20, offset: int = 0):
        """
        Get a list of the playlists owned or followed by a user.

        Parameters:
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('users/{}/playlists'.format(user_id), limit=limit, offset=offset)

    def playlist(self, playlist_id: str, fields: str = None, market: str = 'from_token'):
        """
        Get playlist of a user.

        Parameters:
            - playlist - the id of the playlist
            - fields - which fields to return
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('playlists/' + playlist_id, fields=fields, market=market)

    def playlist_cover_image(self, playlist_id: str):
        return self._get('playlists/{}/images'.format(playlist_id))

    def playlist_cover_image_upload(self, playlist_id: str):
        pass
        # Content type: image/jpg
        # Body: base64 image, max 256 KB
        # return self._put('playlists/{}/images'.format(playlist_id))

    def playlist_tracks(self, playlist_id: str, fields: str = None,
                        market: str = 'from_token', limit: int = 100, offset: int = 0):
        """
        Get full details of the tracks of a playlist owned by a user.

        Parameters:
            - playlist_id - playlist ID
            - fields - which fields to return
            - limit - the number of items to return (1..100)
            - offset - the index of the first item to return
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('playlists/{}/tracks'.format(playlist_id),
                         limit=limit, offset=offset, fields=fields, market=market)

    def playlist_create(self, user_id: str, name: str, public: bool = True, description: str = ''):
        """
        Create a playlist for a user.

        Parameters:
            - user_id - the id of the user
            - name - the name of the playlist
            - public - is the created playlist public
            - description - the description of the playlist
        """
        payload = {
            'name': name,
            'public': public,
            'description': description
        }
        return self._post('users/{}/playlists'.format(user_id), payload=payload)

    def playlist_change_details(self, playlist_id: str, name: str = None, public: bool = None,
                                collaborative: bool = None, description: str = None):
        """
        Changes a playlist's name and/or public/private state.

        Parameters:
            - playlist_id - playlist ID
            - name - optional name of the playlist
            - public - optional is the playlist public
            - collaborative - optional is the playlist collaborative
            - description - optional description of the playlist
        """
        data = {
            'name': name,
            'public': public,
            'collaborative': collaborative,
            'description': description,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self._put('playlists/' + playlist_id, payload=data)

    def playlist_tracks_add(self, playlist_id: str, track_ids: list, position: int = None):
        """
        Add tracks to a playlist.

        Parameters:
            - playlist_id - playlist ID
            - track_ids - list of track IDs
            - position - position to add the tracks
        """
        payload = {'uris': [to_uri('track', t) for t in track_ids]}
        return self._post('playlists/{}/tracks'.format(playlist_id), payload=payload, position=position)

    def playlist_tracks_replace(self, playlist_id: str, track_ids: list):
        """
        Replace all tracks in a playlist

        Parameters:
            - playlist_id - playlist ID
            - track_ids - list of track IDs to add to the playlist
        """
        payload = {'uris': [to_uri('track', t) for t in track_ids]}
        return self._put('playlists/{}/tracks'.format(playlist_id), payload=payload)

    def playlist_tracks_reorder(self, playlist_id: str, range_start: int, insert_before: int,
                                range_length: int = 1, snapshot_id: str = None):
        """
        Reorder tracks in a playlist.

        Parameters:
            - playlist_id - playlist ID
            - range_start - position of the first track to be reordered
            - range_length - optional the number of tracks to be reordered (default: 1)
            - insert_before - position where the tracks should be inserted
            - snapshot_id - optional playlist's snapshot ID
        """
        payload = {
            'range_start': range_start,
            'range_length': range_length,
            'insert_before': insert_before
        }
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._put('playlists/{}/tracks'.format(playlist_id), payload=payload)

    def playlist_tracks_remove(self, playlist_id: str, track_ids: list, snapshot_id=None):
        """
        Remove all occurrences of tracks from a playlist.

        Parameters:
            - playlist_id - playlist ID
            - track_ids - list of track IDs to add to the playlist
            - snapshot_id - optional playlist's snapshot ID
        """
        tracks = [to_uri('track', t) for t in track_ids]
        payload = {'tracks': [{'uri': t} for t in tracks]}
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._delete('playlists/{}/tracks'.format(playlist_id), payload=payload)

    def playlist_tracks_remove_occurrences(self, playlist_id: str, tracks: list, snapshot_id=None):
        """
        Removes all occurrences of the given tracks from the given playlist

        Parameters:
            - playlist_id - playlist ID
            - track_ids - an array of objects containing Spotify URIs of the tracks
            to remove with their current positions in the playlist. For example:
                [  { "uri":"4iV5W9uYEdYUVa79Axb7Rh", "positions":[2] },
                   { "uri":"1301WleyT98MSxVHPZCA6M", "positions":[7] } ]
            - snapshot_id - optional id of the playlist snapshot
        """
        ftracks = []
        for tr in tracks:
            ftracks.append({
                'uri': to_uri('track', tr['uri']),
                'positions': tr['positions'],
            })
        payload = {'tracks': ftracks}
        if snapshot_id:
            payload['snapshot_id'] = snapshot_id
        return self._delete('playlists/{}/tracks'.format(playlist_id), payload=payload)
