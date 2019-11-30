from spotipy.client.player.modify import SpotifyPlayerModify
from spotipy.client.player.view import SpotifyPlayerView


class SpotifyPlayer(SpotifyPlayerModify, SpotifyPlayerView):
    pass
