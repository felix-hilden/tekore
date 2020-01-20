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
        self.token, old_token = token, self.token
        yield self
        self.token = old_token
