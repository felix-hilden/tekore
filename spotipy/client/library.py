from spotipy.client.base import SpotifyBase


class SpotifyLibrary(SpotifyBase):
    def current_user_albums(self, market: str = 'from_token', limit: int = 20,
                            offset: int = 0):
        """
        Get a list of the albums saved in the current user's Your Music
        library.
        Requires the user-libray-read scope.

        Parameters:
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('me/albums', market=market, limit=limit,
                         offset=offset)

    def current_user_albums_contains(self, album_ids: list):
        """
        Check if user has saved albums.
        Requires the user-library-read scope.

        Parameters:
            - album_ids - list of album IDs
        """
        return self._get('me/albums/contains?ids=' + ','.join(album_ids))

    def current_user_albums_add(self, album_ids: list):
        """
        Save albums for current user.
        Requires the user-library-modify scope.

        Parameters:
            - album_ids - list of album IDs
        """
        return self._put('me/albums?ids=' + ','.join(album_ids))

    def current_user_albums_delete(self, album_ids: list):
        """
        Remove albums for current user.
        Requires the user-library-modify scope.

        Parameters:
            - album_ids - list of album IDs
        """
        return self._delete('me/albums?ids=' + ','.join(album_ids))

    def current_user_tracks(self, market: str = 'from_token', limit: int = 20,
                            offset: int = 0):
        """
        Get a list of the songs saved in the current user's Your Music library.
        Requires the user-libray-read scope.

        Parameters:
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('me/tracks', market=market, limit=limit,
                         offset=offset)

    def current_user_tracks_contains(self, track_ids: list):
        """
        Check if user has saved tracks.
        Requires the user-library-read scope.

        Parameters:
            - track_ids - list of track IDs
        """
        return self._get('me/tracks/contains?ids=' + ','.join(track_ids))

    def current_user_tracks_add(self, track_ids: list):
        """
        Save tracks for current user.
        Requires the user-library-modify scope.

        Parameters:
            - track_ids - list of track IDs
        """
        return self._put('me/tracks/?ids=' + ','.join(track_ids))

    def current_user_tracks_delete(self, track_ids: list):
        """
        Remove tracks for current user.
        Requires the user-library-modify scope.

        Parameters:
            - track_ids - list of track IDs
        """
        return self._delete('me/tracks/?ids=' + ','.join(track_ids))
