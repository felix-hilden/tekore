from collections.abc import Generator
from contextlib import contextmanager

from .api import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyAudiobook,
    SpotifyBrowse,
    SpotifyChapter,
    SpotifyEpisode,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyMarkets,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyShow,
    SpotifyTrack,
    SpotifyUser,
)
from .paging import SpotifyPaging
from .short_link import SpotifyShortLink


class Spotify(
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyAudiobook,
    SpotifyBrowse,
    SpotifyChapter,
    SpotifyEpisode,
    SpotifyFollow,
    SpotifyLibrary,
    SpotifyMarkets,
    SpotifyPersonalisation,
    SpotifyPlayer,
    SpotifyPlaylist,
    SpotifySearch,
    SpotifyShow,
    SpotifyTrack,
    SpotifyUser,
    SpotifyPaging,
    SpotifyShortLink,
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
    def token_as(self, token) -> Generator["Spotify", None, None]:
        """
        Use a different token with requests. Context manager, async safe.

        Parameters
        ----------
        token
            access token

        Returns
        -------
        Generator[Spotify, None, None]
            self as context

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
        cv_token = self._token_cv.set(token)
        yield self
        self._token_cv.reset(cv_token)

    @contextmanager
    def max_limits(self, on: bool = True) -> Generator["Spotify", None, None]:
        """
        Toggle using maximum limits in paging calls. Context manager, async safe.

        Parameters
        ----------
        on
            enable or disable using maximum limits

        Returns
        -------
        Generator[Spotify, None, None]
            self as context

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
        cv_token = self._max_limits_on_cv.set(on)
        yield self
        self._max_limits_on_cv.reset(cv_token)

    @contextmanager
    def chunked(self, on: bool = True) -> Generator["Spotify", None, None]:
        """
        Toggle chunking lists of resources. Context manager, async safe.

        Parameters
        ----------
        on
            enable or disable chunking

        Returns
        -------
        Generator[Spotify, None, None]
            self as context

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
        cv_token = self._chunked_on_cv.set(on)
        yield self
        self._chunked_on_cv.reset(cv_token)
