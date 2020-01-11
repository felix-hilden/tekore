from spotipy.client.api.playlist.modify import SpotifyPlaylistModify
from spotipy.client.api.playlist.tracks import SpotifyPlaylistTracks
from spotipy.client.api.playlist.view import SpotifyPlaylistView


class SpotifyPlaylist(
    SpotifyPlaylistView,
    SpotifyPlaylistModify,
    SpotifyPlaylistTracks
):
    pass
