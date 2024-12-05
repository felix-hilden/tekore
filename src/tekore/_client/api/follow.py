from __future__ import annotations

from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists, return_none
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import nothing, single
from tekore.model import FullArtistCursorPaging


class SpotifyFollow(SpotifyBase):
    """Follow API endpoints."""

    @scopes(optional=[scope.playlist_read_private])
    @chunked("user_ids", 2, 5, join_lists)
    @send_and_process(nothing)
    def playlist_is_following(
        self, playlist_id: str, user_ids: list[str]
    ) -> list[bool]:
        """
        Check if users are following a playlist.

        Parameters
        ----------
        playlist_id
            playlist ID
        user_ids
            list of user IDs, max 5 without chunking

        Returns
        -------
        list[bool]
            follow statuses in the same order that the user IDs were given
        """
        return self._get(
            f"playlists/{playlist_id}/followers/contains", ids=",".join(user_ids)
        )

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
    def playlist_follow(self, playlist_id: str, public: bool = True) -> None:
        """
        Follow a playlist as current user.

        Parameters
        ----------
        playlist_id
            playlist ID
        public
            follow publicly
        """
        payload = {"public": public}
        return self._put(f"playlists/{playlist_id}/followers", payload=payload)

    @scopes([scope.playlist_modify_public], [scope.playlist_modify_private])
    @send_and_process(nothing)
    def playlist_unfollow(self, playlist_id: str) -> None:
        """
        Unfollow a playlist as current user.

        Parameters
        ----------
        playlist_id
            playlist ID
        """
        return self._delete(f"playlists/{playlist_id}/followers")

    @scopes([scope.user_follow_read])
    @send_and_process(single(FullArtistCursorPaging, from_item="artists"))
    @maximise_limit(50)
    def followed_artists(
        self, limit: int = 20, after: str | None = None
    ) -> FullArtistCursorPaging:
        """
        Get artists followed by the current user.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        after
            the last artist ID retrieved from the previous request
        """
        return self._get("me/following", type="artist", limit=limit, after=after)

    @scopes([scope.user_follow_read])
    @chunked("artist_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def artists_is_following(self, artist_ids: list[str]) -> list[bool]:
        """
        Check if current user follows artists.

        Parameters
        ----------
        artist_ids
            list of artist IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            follow statuses in the same order that the artist IDs were given
        """
        return self._get(
            "me/following/contains", type="artist", ids=",".join(artist_ids)
        )

    @scopes([scope.user_follow_modify])
    @chunked("artist_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def artists_follow(self, artist_ids: list[str]) -> None:
        """
        Follow artists as current user.

        Parameters
        ----------
        artist_ids
            list of artist IDs, max 50 without chunking
        """
        return self._put("me/following", type="artist", ids=",".join(artist_ids))

    @scopes([scope.user_follow_modify])
    @chunked("artist_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def artists_unfollow(self, artist_ids: list[str]) -> None:
        """
        Unfollow artists as current user.

        Parameters
        ----------
        artist_ids
            list of artist IDs, max 50 without chunking
        """
        return self._delete("me/following", type="artist", ids=",".join(artist_ids))

    @scopes([scope.user_follow_read])
    @chunked("user_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def users_is_following(self, user_ids: list[str]) -> list[bool]:
        """
        Check if current user follows users.

        Parameters
        ----------
        user_ids
            list of user IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            follow statuses in the same order that the user IDs were given
        """
        return self._get("me/following/contains", type="user", ids=",".join(user_ids))

    @scopes([scope.user_follow_modify])
    @chunked("user_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def users_follow(self, user_ids: list[str]) -> None:
        """
        Follow users as current user.

        Parameters
        ----------
        user_ids
            list of user IDs, max 50 without chunking
        """
        return self._put("me/following", type="user", ids=",".join(user_ids))

    @scopes([scope.user_follow_modify])
    @chunked("user_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def users_unfollow(self, user_ids: list[str]) -> None:
        """
        Unfollow users as current user.

        Parameters
        ----------
        user_ids
            list of user IDs, max 50 without chunking
        """
        return self._delete("me/following", type="user", ids=",".join(user_ids))
