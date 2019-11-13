from typing import Union

from spotipy.client.album import SpotifyAlbum
from spotipy.client.artist import SpotifyArtist
from spotipy.client.browse import SpotifyBrowse
from spotipy.client.follow import SpotifyFollow
from spotipy.client.library import SpotifyLibrary
from spotipy.client.player import SpotifyPlayer
from spotipy.client.playlist import SpotifyPlaylist
from spotipy.client.track import SpotifyTrack

from spotipy.model import (
    FullArtistOffsetPaging,
    FullTrackPaging,
    SimpleAlbumPaging,
    SimplePlaylistPaging,
    PublicUser,
    PrivateUser
)


paging_type = {
    'artist': FullArtistOffsetPaging,
    'album': SimpleAlbumPaging,
    'playlist': SimplePlaylistPaging,
    'track': FullTrackPaging,
}


class Spotify(
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifyTrack
):

    def search(
            self,
            query: str,
            types: tuple = ('track',),
            market: str = None,
            include_external: str = None,
            limit: int = 20,
            offset: int = 0
    ):
        """
        Search for an item.

        Requires the user-read-private scope.

        Parameters
        ----------
        query
            search query
        types
            items to return: 'artist', 'album', 'track' and/or 'playlist'
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return
        include_external
            if 'audio', response will include any externally hosted audio

        Returns
        -------
        tuple
            paging objects containing the types of items searched for
            in the order that they were specified in 'types'
        """
        json = self._get(
            'search',
            q=query,
            type=','.join(types),
            market=market,
            include_external=include_external,
            limit=limit,
            offset=offset
        )
        return tuple(paging_type[t](**json[t + 's']) for t in types)

    def user(self, user_id: str) -> PublicUser:
        """
        Get a user's profile.

        Parameters
        ----------
        user_id
            user ID

        Returns
        -------
        PublicUser
            public user information
        """
        json = self._get('users/' + user_id)
        return PublicUser(**json)

    def current_user(self) -> PrivateUser:
        """
        Get current user's profile.

        Requires the user-read-private scope to return
        user's country and product subscription level.
        Requires the user-read-email scope to return user's email.

        Returns
        -------
        PrivateUser
            private user information
        """
        json = self._get('me/')
        return PrivateUser(**json)

    def current_user_top_artists(
            self,
            time_range: str = 'medium_term',
            limit: int = 20,
            offset: int = 0
    ) -> FullArtistOffsetPaging:
        """
        Get the current user's top artists.

        Requires the user-top-read scope.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        FullArtistOffsetPaging
            paging object containing artists
        """
        json = self._get(
            'me/top/artists',
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        return FullArtistOffsetPaging(**json)

    def current_user_top_tracks(
            self,
            time_range: str = 'medium_term',
            limit: int = 20,
            offset: int = 0
    ) -> FullTrackPaging:
        """
        Get the current user's top tracks.

        Requires the user-top-read scope.

        Parameters
        ----------
        time_range
            Over what time frame are the affinities computed.
            Valid-values: short_term, medium_term, long_term
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        FullTrackPaging
            paging object containing full tracks
        """
        json = self._get(
            'me/top/tracks',
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        return FullTrackPaging(**json)
