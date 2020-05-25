from .modify import SpotifyPlayerModify
from .view import SpotifyPlayerView


class SpotifyPlayer(SpotifyPlayerModify, SpotifyPlayerView):
    """All player API endpoints."""
