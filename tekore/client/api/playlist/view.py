from typing import Union, Callable
from functools import wraps

from tekore.client.chunked import _get_arg
from tekore.client.process import single, model_list, nothing
from tekore.client.decor import send_and_process, maximise_limit
from tekore.client.base import SpotifyBase
from tekore.serialise import ModelList
from tekore.model import (
    SimplePlaylistPaging,
    FullPlaylist,
    Image,
    PlaylistTrackPaging
)


def process_if_not_specified(post_func: Callable, *arguments) -> Callable:
    """
    Decorate a function to process only if any of arguments is not specified.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    arguments
        arguments to check, tuples of (name, position in argument list)
    """
    def decorator(function: Callable) -> Callable:
        async def async_wrapper(self, *args, **kwargs):
            json = await function(self, *args, **kwargs)
            return post_func(json)

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            not_none = [
                _get_arg(arg_pos - 1, arg_name, args, kwargs) is not None
                for arg_name, arg_pos in arguments
            ]
            if any(not_none):
                return function(self, *args, **kwargs)

            if self.is_async:
                return async_wrapper(self, *args, **kwargs)

            json = function(self, *args, **kwargs)
            return post_func(json)
        return wrapper
    return decorator


class SpotifyPlaylistView(SpotifyBase):
    @send_and_process(single(SimplePlaylistPaging))
    @maximise_limit(50)
    def followed_playlists(
            self,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by the current user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope
        to return collaborative playlists.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        return self._get('me/playlists', limit=limit, offset=offset)

    @send_and_process(single(SimplePlaylistPaging))
    @maximise_limit(50)
    def playlists(
            self,
            user_id: str,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by a user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope to return collaborative
        playlists. Collaborative playlists are only returned for current user.

        Parameters
        ----------
        user_id
            user ID
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        return self._get(
            f'users/{user_id}/playlists',
            limit=limit,
            offset=offset
        )

    @process_if_not_specified(
        single(FullPlaylist),
        ('fields', 2),
        ('episodes_as_tracks', 4)
    )
    @send_and_process(nothing)
    def playlist(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = None,
            episodes_as_tracks: bool = None,
    ) -> Union[FullPlaylist, dict]:
        """
        Get playlist of a user.

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
        episodes_as_tracks
            if True, return episodes as objects with track-like fields

        Returns
        -------
        Union[FullPlaylist, dict]
            playlist object, or raw dictionary
            if ``fields`` or ``episodes_as_tracks`` was specified
        """
        if episodes_as_tracks is True:
            additional_types = None
        else:
            additional_types = 'track,episode'

        return self._get(
            'playlists/' + playlist_id,
            fields=fields,
            market=market,
            additional_types=additional_types,
        )

    @send_and_process(model_list(Image))
    def playlist_cover_image(self, playlist_id: str) -> ModelList:
        """
        Get cover image of a playlist. Note: returns a list of images.

        Parameters
        ----------
        playlist_id
            playlist ID

        Returns
        -------
        ModelList
            list of cover images
        """
        return self._get(f'playlists/{playlist_id}/images')

    @process_if_not_specified(
        single(PlaylistTrackPaging),
        ('fields', 2),
        ('episodes_as_tracks', 4)
    )
    @send_and_process(nothing)
    def playlist_tracks(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = None,
            episodes_as_tracks: bool = False,
            limit: int = 100,
            offset: int = 0
    ) -> Union[PlaylistTrackPaging, dict]:
        """
        Get full details of the tracks of a playlist owned by a user.

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
        episodes_as_tracks
            if True, return episodes as objects with track-like fields
        limit
            the number of items to return (1..100)
        offset
            the index of the first item to return

        Returns
        -------
        Union[PlaylistTrackPaging, dict]
            paging object containing playlist tracks, or raw dictionary
            if ``fields`` or ``episodes_as_tracks`` was specified
        """
        if episodes_as_tracks is True:
            additional_types = None
        else:
            additional_types = 'track,episode'

        return self._get(
            f'playlists/{playlist_id}/tracks',
            limit=limit,
            offset=offset,
            fields=fields,
            market=market,
            additional_types=additional_types,
        )
