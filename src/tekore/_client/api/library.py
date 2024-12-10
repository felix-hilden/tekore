from __future__ import annotations

from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists, return_none
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import nothing, single
from tekore.model import (
    SavedAlbumPaging,
    SavedEpisodePaging,
    SavedShowPaging,
    SavedTrackPaging,
)


class SpotifyLibrary(SpotifyBase):
    """Library API endpoints."""

    @scopes([scope.user_library_read])
    @send_and_process(single(SavedAlbumPaging))
    @maximise_limit(50)
    def saved_albums(
        self, market: str | None = None, limit: int = 20, offset: int = 0
    ) -> SavedAlbumPaging:
        """
        Get the albums saved in the current user's library.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get("me/albums", market=market, limit=limit, offset=offset)

    @scopes([scope.user_library_read])
    @chunked("album_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_albums_contains(self, album_ids: list[str]) -> list[bool]:
        """
        Check if user has saved albums.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            save statuses in the same order the album IDs were given
        """
        return self._get("me/albums/contains", ids=",".join(album_ids))

    @scopes([scope.user_library_modify])
    @chunked("album_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_albums_add(self, album_ids: list[str]) -> None:
        """
        Save albums for current user.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking
        """
        return self._put("me/albums", ids=",".join(album_ids))

    @scopes([scope.user_library_modify])
    @chunked("album_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_albums_delete(self, album_ids: list[str]) -> None:
        """
        Remove albums for current user.

        Parameters
        ----------
        album_ids
            list of album IDs, max 50 without chunking
        """
        return self._delete("me/albums", ids=",".join(album_ids))

    @scopes([scope.user_library_read])
    @send_and_process(single(SavedEpisodePaging))
    @maximise_limit(50)
    def saved_episodes(
        self, market: str | None = None, limit: int = 20, offset: int = 0
    ) -> SavedEpisodePaging:
        """
        Get the episodes saved in the current user's library.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get("me/episodes", market=market, limit=limit, offset=offset)

    @scopes([scope.user_library_read])
    @chunked("episode_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_episodes_contains(self, episode_ids: list[str]) -> list[bool]:
        """
        Check if user has saved episodes.

        Parameters
        ----------
        episode_ids
            list of episode IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            save statuses in the same order the episode IDs were given
        """
        return self._get("me/episodes/contains", ids=",".join(episode_ids))

    @scopes([scope.user_library_modify])
    @chunked("episode_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_episodes_add(self, episode_ids: list[str]) -> None:
        """
        Save episodes for current user.

        Parameters
        ----------
        episode_ids
            list of episode IDs, max 50 without chunking
        """
        return self._put("me/episodes", ids=",".join(episode_ids))

    @scopes([scope.user_library_modify])
    @chunked("episode_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_episodes_delete(self, episode_ids: list[str]) -> None:
        """
        Remove episodes for current user.

        Parameters
        ----------
        episode_ids
            list of episode IDs, max 50 without chunking
        """
        return self._delete("me/episodes", ids=",".join(episode_ids))

    @scopes([scope.user_library_read])
    @send_and_process(single(SavedTrackPaging))
    @maximise_limit(50)
    def saved_tracks(
        self, market: str | None = None, limit: int = 20, offset: int = 0
    ) -> SavedTrackPaging:
        """
        Get the songs saved in the current user's library.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get("me/tracks", market=market, limit=limit, offset=offset)

    @scopes([scope.user_library_read])
    @chunked("track_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_tracks_contains(self, track_ids: list[str]) -> list[bool]:
        """
        Check if user has saved tracks.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            save statuses in the same order the track IDs were given
        """
        return self._get("me/tracks/contains", ids=",".join(track_ids))

    @scopes([scope.user_library_modify])
    @chunked("track_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_tracks_add(self, track_ids: list[str]) -> None:
        """
        Save tracks for current user.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking
        """
        return self._put("me/tracks", ids=",".join(track_ids))

    @scopes([scope.user_library_modify])
    @chunked("track_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_tracks_delete(self, track_ids: list[str]) -> None:
        """
        Remove tracks for current user.

        Parameters
        ----------
        track_ids
            list of track IDs, max 50 without chunking
        """
        return self._delete("me/tracks", ids=",".join(track_ids))

    @scopes([scope.user_library_read])
    @send_and_process(single(SavedShowPaging))
    @maximise_limit(50)
    def saved_shows(
        self, market: str | None = None, limit: int = 20, offset: int = 0
    ) -> SavedShowPaging:
        """
        Get the shows saved in the current user's library.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get("me/shows", market=market, limit=limit, offset=offset)

    @scopes([scope.user_library_read])
    @chunked("show_ids", 1, 50, join_lists)
    @send_and_process(nothing)
    def saved_shows_contains(self, show_ids: list[str]) -> list[bool]:
        """
        Check if user has saved shows.

        Parameters
        ----------
        show_ids
            list of show IDs, max 50 without chunking

        Returns
        -------
        list[bool]
            save statuses in the same order the show IDs were given
        """
        return self._get("me/shows/contains", ids=",".join(show_ids))

    @scopes([scope.user_library_modify])
    @chunked("show_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_shows_add(self, show_ids: list[str]) -> None:
        """
        Save shows for current user.

        Parameters
        ----------
        show_ids
            list of show IDs, max 50 without chunking
        """
        return self._put("me/shows", ids=",".join(show_ids))

    @scopes([scope.user_library_modify])
    @chunked("show_ids", 1, 50, return_none)
    @send_and_process(nothing)
    def saved_shows_delete(
        self, show_ids: list[str], market: str | None = None
    ) -> None:
        """
        Remove shows for current user.

        Parameters
        ----------
        show_ids
            list of show IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code, only remove shows that are
            available in the specified market, overrided by token's country
        """
        return self._delete("me/shows", ids=",".join(show_ids), market=market)
