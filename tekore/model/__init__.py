"""
Response model definitions for :mod:`client <tekore.client>`.

Responses are parsed into model classes.
This allows accessing parts of the response directly as attributes.

.. code:: python

    from tekore import Spotify

    # Call the API
    spotify = Spotify(token)
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')

    # Use the response
    for track in album.tracks.items:
        print(track.track_number, track.name)

Additional features of response models are documented in
:mod:`serialise <tekore.serialise>`.

Base classes
------------
Base classes for some of the models.

.. automodule:: tekore.model.base
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Album-related
-------------
.. automodule:: tekore.model.album.base
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.album
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.album.full
   :members:
   :undoc-members:
   :show-inheritance:

Artist-related
--------------
.. automodule:: tekore.model.artist
   :members:
   :undoc-members:
   :show-inheritance:

Errors
------
.. automodule:: tekore.model.error
   :members:
   :undoc-members:
   :show-inheritance:

Paging
------
.. automodule:: tekore.model.paging
   :members:
   :undoc-members:
   :show-inheritance:

Playback-related
----------------

Currently playing
*****************
.. automodule:: tekore.model.currently_playing
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.device
   :members:
   :undoc-members:
   :show-inheritance:

Play history
************
.. automodule:: tekore.model.play_history
   :members:
   :undoc-members:
   :show-inheritance:

Playlist-related
----------------
.. automodule:: tekore.model.playlist
   :members:
   :undoc-members:
   :show-inheritance:

Local items
***********
Some playlists contain locally stored tracks.
They contain mostly `None` values along with empty lists and dictionaries.

.. automodule:: tekore.model.local
   :members:
   :undoc-members:
   :show-inheritance:

Track-related
-------------
.. automodule:: tekore.model.track
   :members:
   :undoc-members:
   :show-inheritance:

Audio analysis
**************
.. automodule:: tekore.model.audio_analysis
   :members:
   :undoc-members:
   :show-inheritance:

Audio features
**************

.. automodule:: tekore.model.audio_features
   :members:
   :undoc-members:
   :show-inheritance:

User
----
.. automodule:: tekore.model.user
   :members:
   :undoc-members:
   :show-inheritance:

Miscellaneous
-------------
.. automodule:: tekore.model.category
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.context
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.member
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: tekore.model.recommendations
   :members:
   :undoc-members:
   :show-inheritance:

"""

from tekore.model.album import SimpleAlbumPaging, AlbumGroup
from tekore.model.album.full import FullAlbum, SavedAlbumPaging
from tekore.model.artist import (
    FullArtist,
    FullArtistCursorPaging,
    FullArtistOffsetPaging,
)
from tekore.model.audio_analysis import AudioAnalysis
from tekore.model.audio_features import AudioFeatures
from tekore.model.category import Category, CategoryPaging
from tekore.model.currently_playing import (
    CurrentlyPlayingContext,
    CurrentlyPlaying,
    RepeatState,
)
from tekore.model.device import Device
from tekore.model.error import PlayerErrorReason
from tekore.model.member import Image
from tekore.model.play_history import PlayHistoryPaging
from tekore.model.playlist import (
    PlaylistTrackPaging,
    FullPlaylist,
    SimplePlaylistPaging,
)
from tekore.model.recommendations import Recommendations, RecommendationAttribute
from tekore.model.track import (
    FullTrack,
    SimpleTrackPaging,
    SavedTrackPaging,
    FullTrackPaging,
)
from tekore.model.user import PrivateUser, PublicUser
