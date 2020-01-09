"""
Response models from the :mod:`client <spotipy.client>`.

Responses are parsed into model classes.
This allows accessing parts of the response directly as attributes.

.. code:: python

    from spotipy import Spotify

    # Call the API
    spotify = Spotify(token)
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')

    # Use the response
    for track in album.tracks.items:
        print(track.track_number, track.name)

Base classes
------------
Base classes for some of the models.

.. automodule:: spotipy.model.base
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Album-related
-------------
.. automodule:: spotipy.model.album.base
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.album
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.album.full
   :members:
   :undoc-members:
   :show-inheritance:

Artist-related
--------------
.. automodule:: spotipy.model.artist
   :members:
   :undoc-members:
   :show-inheritance:

Errors
------
.. automodule:: spotipy.model.error
   :members:
   :undoc-members:
   :show-inheritance:

Paging
------
.. automodule:: spotipy.model.paging
   :members:
   :undoc-members:
   :show-inheritance:

Playback-related
----------------

Currently playing
*****************
.. automodule:: spotipy.model.currently_playing
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.device
   :members:
   :undoc-members:
   :show-inheritance:

Play history
************
.. automodule:: spotipy.model.play_history
   :members:
   :undoc-members:
   :show-inheritance:

Playlist-related
----------------
.. automodule:: spotipy.model.playlist
   :members:
   :undoc-members:
   :show-inheritance:

Local items
***********
Some playlists contain locally stored tracks.
They contain mostly `None` values along with empty lists and dictionaries.

.. automodule:: spotipy.model.local
   :members:
   :undoc-members:
   :show-inheritance:

Track-related
-------------
.. automodule:: spotipy.model.track
   :members:
   :undoc-members:
   :show-inheritance:

Audio analysis
**************
.. automodule:: spotipy.model.audio_analysis
   :members:
   :undoc-members:
   :show-inheritance:

Audio features
**************

.. automodule:: spotipy.model.audio_features
   :members:
   :undoc-members:
   :show-inheritance:

User
----
.. automodule:: spotipy.model.user
   :members:
   :undoc-members:
   :show-inheritance:

Miscellaneous
-------------
.. automodule:: spotipy.model.category
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.context
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.member
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: spotipy.model.recommendations
   :members:
   :undoc-members:
   :show-inheritance:

"""

from spotipy.model.album import SimpleAlbumPaging, AlbumGroup
from spotipy.model.album.full import FullAlbum, SavedAlbumPaging
from spotipy.model.artist import (
    FullArtist,
    FullArtistCursorPaging,
    FullArtistOffsetPaging,
)
from spotipy.model.audio_analysis import AudioAnalysis
from spotipy.model.audio_features import AudioFeatures
from spotipy.model.category import Category, CategoryPaging
from spotipy.model.currently_playing import (
    CurrentlyPlayingContext,
    CurrentlyPlaying,
    RepeatState,
)
from spotipy.model.device import Device
from spotipy.model.error import PlayerErrorReason
from spotipy.model.member import Image
from spotipy.model.play_history import PlayHistoryPaging
from spotipy.model.playlist import (
    PlaylistTrackPaging,
    FullPlaylist,
    SimplePlaylistPaging,
)
from spotipy.model.recommendations import Recommendations, RecommendationAttribute
from spotipy.model.track import (
    FullTrack,
    SimpleTrackPaging,
    SavedTrackPaging,
    FullTrackPaging,
)
from spotipy.model.user import PrivateUser, PublicUser
