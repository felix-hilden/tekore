from contextlib import contextmanager

from .paging import SpotifyPaging
from .api import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyEpisode,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyShow,
    SpotifyTrack,
    SpotifyUser,
)


class Spotify(
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyBrowse,
    SpotifyEpisode,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyShow,
    SpotifyTrack,
    SpotifyUser,
    SpotifyPaging,
):
    """
    Bases: :class:`tekore.Client`.

    Client to Web API endpoints.

    Parameters
    ----------
    token
        bearer token for requests
    sender
        request sender
    asynchronous
        synchronicity requirement
    max_limits_on
        use maximum limits in paging calls, overrided by endpoint arguments
    chunked_on
        use chunking when requesting lists of resources

    Attributes
    ----------
    token
        bearer token for requests
    sender
        underlying sender
    max_limits_on
        use maximum limits in paging calls, overrided by endpoint arguments
    chunked_on
        use chunking when requesting lists of resources
    """

    @contextmanager
    def token_as(self, token) -> 'Spotify':
        """
        Use a different token with requests. Context manager.

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
        Toggle using maximum limits in paging calls. Context manager.

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

    @contextmanager
    def chunked(self, on: bool = True) -> 'Spotify':
        """
        Toggle chunking lists of resources. Context manager.

        Parameters
        ----------
        on
            enable or disable chunking

        Returns
        -------
        Spotify
            self

        Examples
        --------
        .. code:: python

            spotify = Spotify(token)
            with spotify.chunked(True):
                tracks = spotify.tracks(many_ids)

            spotify = Spotify(token, chunked_on=True)
            with spotify.chunked(False):
                tracks = spotify.search(many_ids[:50])
        """
        self.chunked_on, old = on, self.chunked_on
        yield self
        self.chunked_on = old
