from spotipy.client.api.player.modify import SpotifyPlayerModify
from spotipy.client.api.player.view import SpotifyPlayerView


class SpotifyPlayer(SpotifyPlayerModify, SpotifyPlayerView):
    pass
