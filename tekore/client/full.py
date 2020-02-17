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
        Temporarily use a different token with requests.

        Parameters
        ----------
        token
            access token

        Returns
        -------
        Spotify
            self
        """
        self.token, old = token, self.token
        yield self
        self.token = old

    @contextmanager
    def max_limits(self, on: bool = True) -> 'Spotify':
        """
        Temporarily toggle using maximum limits in paging calls.

        Parameters
        ----------
        on
            enable or disable using maximum limits

        Returns
        -------
        Spotify
            self
        """
        self.max_limits_on, old = on, self.max_limits_on
        yield self
        self.max_limits_on = old
