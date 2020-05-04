from .modify import SpotifyPlaylistModify
from .tracks import SpotifyPlaylistTracks
from .view import SpotifyPlaylistView


class SpotifyPlaylist(
    SpotifyPlaylistView,
    SpotifyPlaylistModify,
    SpotifyPlaylistTracks
):
    pass
