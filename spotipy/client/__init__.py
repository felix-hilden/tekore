from spotipy.client.album import SpotifyAlbum
from spotipy.client.artist import SpotifyArtist
from spotipy.client.browse import SpotifyBrowse
from spotipy.client.follow import SpotifyFollow
from spotipy.client.library import SpotifyLibrary
from spotipy.client.player import SpotifyPlayer
from spotipy.client.playlist import SpotifyPlaylist
from spotipy.client.track import SpotifyTrack


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

    def search(self, q: str, type_: str = 'track', market: str = 'from_token',
               include_external: str = None, limit: int = 20, offset: int = 0):
        """
        Search for an item.
        Requires the user-read-private scope.

        Parameters:
            - q - search query
            - type_ - the type of item to return. 'artist', 'album',
                      'track' or 'playlist'
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
            - limit  - the number of items to return (1..50)
            - offset - the index of the first item to return
            - include_external - if 'audio', response will include any
                                 externally hosted audio
        """
        return self._get(
            'search', q=q, type=type_, market=market,
            include_external=include_external, limit=limit, offset=offset)

    def user(self, user_id: str):
        return self._get('users/' + user_id)

    def current_user(self):
        """
        Get current user's profile.
        Requires the user-read-private scope.
        Requires the user-read-email scope to return user's email.
        """
        return self._get('me/')

    def current_user_top_artists(self, time_range: str = 'medium_term',
                                 limit: int = 20, offset: int = 0):
        """
        Get the current user's top artists.
        Requires the user-top-read scope.

        Parameters:
            - time_range - Over what time frame are the affinities computed
                           Valid-values: short_term, medium_term, long_term
            - limit  - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('me/top/artists', time_range=time_range,
                         limit=limit, offset=offset)

    def current_user_top_tracks(self, time_range: str = 'medium_term',
                                limit: int = 20, offset: int = 0):
        """
        Get the current user's top tracks.
        Requires the user-top-read scope.

        Parameters:
            - time_range - Over what time frame are the affinities computed
                           Valid-values: short_term, medium_term, long_term
            - limit  - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('me/top/tracks', time_range=time_range, limit=limit,
                         offset=offset)
