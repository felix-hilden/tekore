from contextlib import contextmanager

from tekore.client.paging import SpotifyPaging
from tekore.client.api import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyTrack,
    SpotifyUser,
)


class Spotify(
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyTrack,
    SpotifyUser,
    SpotifyPaging,
):
    @contextmanager
    def token_as(self, token) -> 'Spotify':
        """
        Context manager. Use a different token with requests.

        Parameters
        ----------
        token
            access token

        Returns
        -------
        Spotify
            self

        Examples
        --------
        .. code:: python

            spotify = Spotify()
            with spotify.token_as(token):
                album = spotify.album(album_id)

            spotify = Spotify(app_token)
            with spotify.token_as(user_token):
                user = spotify.current_user()
        """
        self.token, old = token, self.token
        yield self
        self.token = old

    @contextmanager
    def max_limits(self, on: bool = True) -> 'Spotify':
        """
        Context manager. Toggle using maximum limits in paging calls.

        Parameters
        ----------
        on
            enable or disable using maximum limits

        Returns
        -------
        Spotify
            self

        Examples
        --------
        .. code:: python

            spotify = Spotify(token)
            with spotify.max_limits(True):
                tracks, = spotify.search('piano')

            spotify = Spotify(token, max_limits_on=True)
            with spotify.max_limits(False):
                tracks, = spotify.search('piano')
        """
        self.max_limits_on, old = on, self.max_limits_on
        yield self
        self.max_limits_on = old
