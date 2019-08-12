from spotipy.client._base import SpotifyBase


class SpotifyFollow(SpotifyBase):
    def playlist_is_following(self, playlist_id: str, user_ids: list):
        """
        Check to see if the given users are following a playlist.

        Parameters:
            - playlist_id - the id of the playlist
            - user_ids - the ids of the users that you want to check to see if they follow the playlist. Maximum: 5 ids.
        """
        return self._get("playlists/{}/followers/contains?ids={}".format(
            playlist_id, ','.join(user_ids))
        )

    def current_user_playlist_follow(self, playlist_id: str):
        return self._put("playlists/{}/followers".format(playlist_id))

    def current_user_playlist_unfollow(self, playlist_id: str):
        return self._delete("playlists/{}/followers".format(playlist_id))

    def current_user_followed_artists(self, limit: int = 20, after: str = None):
        """
        Get artists followed by the current user.

        Parameters:
            - limit  - the number of items to return (1..50)
            - after - ghe last artist ID retrieved from the previous request
        """
        return self._get('me/following', type='artist', limit=limit, after=after)

    def current_user_artists_is_following(self, artist_ids: list):
        return self._get('me/following/contains?type=artist&ids=' + ','.join(artist_ids))

    def current_user_artists_follow(self, artist_ids: list):
        return self._put('me/following?type=artist&ids=' + ','.join(artist_ids))

    def current_user_artists_unfollow(self, artist_ids: list):
        return self._delete('me/following?type=artist&ids=' + ','.join(artist_ids))

    def current_user_users_is_following(self, user_ids: list):
        return self._get('me/following/contains?type=user&ids=' + ','.join(user_ids))

    def current_user_users_follow(self, user_ids: list):
        return self._put('me/following?type=user&ids=' + ','.join(user_ids))

    def current_user_users_unfollow(self, user_ids: list):
        return self._delete('me/following?type=user&ids=' + ','.join(user_ids))
