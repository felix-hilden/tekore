from typing import List

from tekore.client.process import single, nothing
from tekore.client.base import SpotifyBase, send_and_process
from tekore.model import FullArtistCursorPaging


class SpotifyFollow(SpotifyBase):
    @send_and_process(nothing)
    def playlist_is_following(self, playlist_id: str, user_ids: list) -> List[bool]:
        """
        Check to see if the given users are following a playlist.

        Requires the playlist-read-private scope to check private playlists.

        Parameters
        ----------
        playlist_id
            playlist ID
        user_ids
            list of user IDs (1..5)

        Returns
        -------
        list
            list of booleans in the same order that the user IDs were given
        """
        return self._get(
            f'playlists/{playlist_id}/followers/contains',
            ids=','.join(user_ids)
        )

    @send_and_process(nothing)
    def playlist_follow(
            self,
            playlist_id: str,
            public: bool = True
    ) -> None:
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

    @send_and_process(nothing)
    def playlist_unfollow(self, playlist_id: str) -> None:
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

    @send_and_process(single(FullArtistCursorPaging, top_item='artists'))
    def followed_artists(
            self,
            limit: int = 20,
            after: str = None
    ) -> FullArtistCursorPaging:
        """
        Get artists followed by the current user.

        Requires the user-follow-read scope.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        after
            the last artist ID retrieved from the previous request

        Returns
        -------
        FullArtistCursorPaging
            cursor-based paging object containing a list of full artist objects
        """
        return self._get('me/following', type='artist', limit=limit, after=after)

    @send_and_process(nothing)
    def artists_is_following(self, artist_ids: list) -> List[bool]:
        """
        Check if current user follows artists.

        Requires the user-follow-read scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs

        Returns
        -------
        list
            list of booleans in the same order that the artist IDs were given
        """
        return self._get(
            'me/following/contains',
            type='artist',
            ids=','.join(artist_ids)
        )

    @send_and_process(nothing)
    def artists_follow(self, artist_ids: list) -> None:
        """
        Follow artists as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs
        """
        return self._put('me/following', type='artist', ids=','.join(artist_ids))

    @send_and_process(nothing)
    def artists_unfollow(self, artist_ids: list) -> None:
        """
        Unfollow artists as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        artist_ids
            list of artist IDs
        """
        return self._delete('me/following', type='artist', ids=','.join(artist_ids))

    @send_and_process(nothing)
    def users_is_following(self, user_ids: list) -> List[bool]:
        """
        Check if current user follows users.

        Requires the user-follow-read scope.

        Parameters
        ----------
        user_ids
            list of user IDs

        Returns
        -------
        list
            list of booleans in the same order that the user IDs were given
        """
        return self._get(
            'me/following/contains', type='user', ids=','.join(user_ids)
        )

    @send_and_process(nothing)
    def users_follow(self, user_ids: list) -> None:
        """
        Follow users as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        user_ids
            list of user IDs
        """
        return self._put('me/following', type='user', ids=','.join(user_ids))

    @send_and_process(nothing)
    def users_unfollow(self, user_ids: list) -> None:
        """
        Unfollow users as current user.

        Requires the user-follow-modify scope.

        Parameters
        ----------
        user_ids
            list of user IDs
        """
        return self._delete('me/following', type='user', ids=','.join(user_ids))
