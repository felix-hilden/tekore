from tekore.client.api.playlist.modify import SpotifyPlaylistModify
from tekore.client.api.playlist.tracks import SpotifyPlaylistTracks
from tekore.client.api.playlist.view import SpotifyPlaylistView


class SpotifyPlaylist(
    SpotifyPlaylistView,
    SpotifyPlaylistModify,
    SpotifyPlaylistTracks
):
    pass
