from spotipy.client.base import SpotifyBase


class SpotifyFollow(SpotifyBase):
    def playlist_is_following(self, playlist_id: str, user_ids: list):
        """
        Check to see if the given users are following a playlist.

        Requires the playlist-read-private scope to check private playlists.

        Parameters
        ----------
        playlist_id
            playlist ID
        user_ids
            list of user IDs (1..5)
        """
        return self._get(
            f'playlists/{playlist_id}/followers/contains?ids='
            ','.join(user_ids)
        )

    def current_user_playlist_follow(self, playlist_id: str, public: bool = True):
        """
        Follow a playlist as current user.

        Requires the playlist-modify-public scope.
        Following privately requires the playlist-modify-private scope.

        Parameters
        ----------
        playlist_id
            playlist ID
        public
            follow publicly
        """
        payload = {
            'public': public
        }
        return self._put(f'playlists/{playlist_id}/followers', payload=payload)

    def current_user_playlist_unfollow(self, playlist_id: str):
        """
        Unfollow a playlist as current user.

        Requires the playlist-modify-public scope. Unfollowing a privately
        followed playlist requires the playlist-modify-private scope.

        Parameters
        ----------
        playlist_id
            playlist ID
        """
        return self._delete(f'playlists/{playlist_id}/followers')

    def current_user_followed_artists(self, limit: int = 20, after: str = None):
        """
        Get artists followed by the current user.

        Requires the user-follow-read scope.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        after
            the last artist ID retrieved from the previous request
        """
        return self._get('me/following', type='artist', limit=limit, after=after)

    def current_user_artists_is_following(self, artist_ids: list):
        """
        Check if current user follows artists.

        Requires the user-follow-read scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs
        """
        return self._get(
            'me/following/contains?type=artist&ids=' + ','.join(artist_ids)
        )

    def current_user_artists_follow(self, artist_ids: list):
        """
        Follow artists as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs
        """
        return self._put(
            'me/following?type=artist&ids=' + ','.join(artist_ids)
        )

    def current_user_artists_unfollow(self, artist_ids: list):
        """
        Unfollow artists as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs
        """
        return self._delete(
            'me/following?type=artist&ids=' + ','.join(artist_ids)
        )

    def current_user_users_is_following(self, user_ids: list):
        """
        Check if current user follows users.

        Requires the user-follow-read scope.

        Parameters
        ----------
        user_ids
            list of user IDs
        """
        return self._get(
            'me/following/contains?type=user&ids=' + ','.join(user_ids)
        )

    def current_user_users_follow(self, user_ids: list):
        """
        Follow users as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        user_ids
            list of user IDs
        """
        return self._put('me/following?type=user&ids=' + ','.join(user_ids))

    def current_user_users_unfollow(self, user_ids: list):
        """
        Unfollow users as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        user_ids
            list of user IDs
        """
        return self._delete('me/following?type=user&ids=' + ','.join(user_ids))
