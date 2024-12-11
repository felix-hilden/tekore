from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import wraps

from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.chunked import _get_arg
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import model_list, nothing, single
from tekore.model import FullPlaylist, Image, PlaylistTrackPaging, SimplePlaylistPaging


def process_if_not_specified(post_func: Callable, *arguments) -> Callable:
    """
    Decorate a function to process only if any of arguments is falsy.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    arguments
        arguments to check, tuples of (name, position in argument list)
    """

    def decorator(function: Callable) -> Callable:
        async def async_wrapper(self: SpotifyBase, *args, **kwargs):
            json = await function(self, *args, **kwargs)
            return post_func(json)

        @wraps(function)
        def wrapper(self: SpotifyBase, *args, **kwargs):
            falsies = [
                bool(_get_arg(arg_pos - 1, arg_name, args, kwargs))
                for arg_name, arg_pos in arguments
            ]
            if any(falsies):
                return function(self, *args, **kwargs)

            if self.is_async:
                return async_wrapper(self, *args, **kwargs)

            json = function(self, *args, **kwargs)
            return post_func(json)

        return wrapper

    return decorator


def parse_additional_types(as_tracks: bool | Iterable[str]) -> str | None:
    """Determine `additional_types` argument content."""
    types = {"track", "episode"}
    if as_tracks is True:
        types = set()
    elif as_tracks is False:
        pass
    else:
        types = types.difference(as_tracks)

    return ",".join(types) if types else None


class SpotifyPlaylistView(SpotifyBase):
    """Playlist API endpoints for viewing playlists."""

    @scopes(optional=[scope.playlist_read_private, scope.playlist_read_collaborative])
    @send_and_process(single(SimplePlaylistPaging))
    @maximise_limit(50)
    def followed_playlists(
        self, limit: int = 20, offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by the current user.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get("me/playlists", limit=limit, offset=offset)

    @scopes(optional=[scope.playlist_read_private, scope.playlist_read_collaborative])
    @send_and_process(single(SimplePlaylistPaging))
    @maximise_limit(50)
    def playlists(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by a user.

        Collaborative playlists are only returned for the current user.

        Parameters
        ----------
        user_id
            user ID
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        """
        return self._get(f"users/{user_id}/playlists", limit=limit, offset=offset)

    @scopes()
    @process_if_not_specified(single(FullPlaylist), ("fields", 2), ("as_tracks", 4))
    @send_and_process(nothing)
    def playlist(
        self,
        playlist_id: str,
        fields: str | None = None,
        market: str | None = None,
        as_tracks: bool | Iterable[str] = False,
    ) -> FullPlaylist | dict:
        """
        Get playlist of a user.

        .. note:: Returns a dictionary if ``fields`` or ``as_tracks`` is specified.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return, see the Web API documentation for details
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
            when using a user token to authenticate.
            For episodes in the playlist, if a user token is used,
            the country associated with it overrides this parameter.
            If an application token is used and no market is specified,
            episodes are considered unavailable and returned as None.
        as_tracks
            return types of items with track-like fields.
            If :class:`True`, return all other types as tracks.
            If an iterable is passed, types contained are returned as tracks.
            Currently the only extra type is ``episode``.

        Returns
        -------
        FullPlaylist | dict
            playlist object, or raw dictionary if ``fields``
            or ``as_tracks`` was specified
        """
        additional_types = parse_additional_types(as_tracks)
        return self._get(
            "playlists/" + playlist_id,
            fields=fields,
            market=market,
            additional_types=additional_types,
        )

    @scopes()
    @send_and_process(model_list(Image))
    def playlist_cover_image(self, playlist_id: str) -> list[Image]:
        """
        Get cover image of a playlist.

        .. note:: Returns a list of images.

        Parameters
        ----------
        playlist_id
            playlist ID
        """
        return self._get(f"playlists/{playlist_id}/images")

    @scopes()
    @process_if_not_specified(
        single(PlaylistTrackPaging), ("fields", 2), ("as_tracks", 4)
    )
    @send_and_process(nothing)
    def playlist_items(
        self,
        playlist_id: str,
        fields: str | None = None,
        market: str | None = None,
        as_tracks: bool | Iterable[str] = False,
        limit: int = 100,
        offset: int = 0,
    ) -> PlaylistTrackPaging | dict:
        """
        Full details of items on a playlist.

        .. note:: Returns a dictionary if ``fields`` or ``as_tracks`` is specified.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return, see the Web API documentation for details
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
            when using a user token to authenticate.
            For episodes in the playlist, if a user token is used,
            the country associated with it overrides this parameter.
            If an application token is used and no market is specified,
            episodes are considered unavailable and returned as None.
        as_tracks
            return types of items with track-like fields.
            If :class:`True`, return all other types as tracks.
            If an iterable is passed, types contained are returned as tracks.
            Currently the only extra type is ``episode``.
        limit
            the number of items to return (1..100)
        offset
            the index of the first item to return

        Returns
        -------
        PlaylistTrackPaging | dict
            paging object containing playlist items, or raw dictionary
            if ``fields`` or ``as_tracks`` was specified
        """
        return self._get(
            f"playlists/{playlist_id}/tracks",
            limit=limit,
            offset=offset,
            fields=fields,
            market=market,
            additional_types=parse_additional_types(as_tracks),
        )
