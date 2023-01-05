from .items import SpotifyPlaylistItems
from .modify import SpotifyPlaylistModify
from .view import SpotifyPlaylistView


class SpotifyPlaylist(SpotifyPlaylistView, SpotifyPlaylistModify, SpotifyPlaylistItems):
    """All playlist API endpoints."""
