from spotipy.client.playlist.modify import SpotifyPlaylistModify
from spotipy.client.playlist.tracks import SpotifyPlaylistTracks
from spotipy.client.playlist.view import SpotifyPlaylistView


class SpotifyPlaylist(
    SpotifyPlaylistView,
    SpotifyPlaylistModify,
    SpotifyPlaylistTracks
):
    pass
