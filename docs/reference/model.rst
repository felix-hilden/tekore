model
=====

Dataclass models are parsed from responses.

Base classes
------------

Base classes for some of the models.

.. autoclass:: spotipy.model.base.Identifiable
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.base.Item
   :members:
   :undoc-members:


Album-related
-------------

.. autoclass:: spotipy.model.album.base.Album
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.SimpleAlbum
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.SimpleAlbumPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.full.FullAlbum
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.full.SavedAlbum
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.full.SavedAlbumPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.base.AlbumType
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.AlbumGroup
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.album.base.ReleaseDatePrecision
   :members:
   :undoc-members:


Artist-related
--------------

.. autoclass:: spotipy.model.artist.Artist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.artist.SimpleArtist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.artist.FullArtist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.artist.FullArtistCursorPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.artist.FullArtistOffsetPaging
   :members:
   :undoc-members:


Errors
------

.. autoclass:: spotipy.model.error.Error
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.error.PlayerError
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.error.PlayerErrorReason
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.error.AuthenticationError
   :members:
   :undoc-members:


Paging
------
.. autoclass:: spotipy.model.paging.Paging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.paging.OffsetPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.paging.Cursor
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.paging.CursorPaging
   :members:
   :undoc-members:


Playback-related
----------------

Currently playing
*****************

.. autoclass:: spotipy.model.currently_playing.CurrentlyPlaying
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.CurrentlyPlayingContext
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.CurrentlyPlayingTrack
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.Actions
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.Disallows
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.CurrentlyPlayingType
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.currently_playing.RepeatState
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.device.Device
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.device.DeviceType
   :members:
   :undoc-members:

Play history
************

.. autoclass:: spotipy.model.play_history.PlayHistory
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.play_history.PlayHistoryPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.play_history.PlayHistoryCursor
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.play_history.MillisecondTimestamp
   :members:
   :undoc-members:


Playlist-related
----------------

.. autoclass:: spotipy.model.playlist.Playlist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.playlist.SimplePlaylist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.playlist.SimplePlaylistPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.playlist.FullPlaylist
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.playlist.PlaylistTrack
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.playlist.PlaylistTrackPaging
   :members:
   :undoc-members:


Track-related
-------------

.. autoclass:: spotipy.model.track.Track
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.SimpleTrack
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.SimpleTrackPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.FullTrack
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.FullTrackPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.TrackLink
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.Tracks
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.SavedTrack
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.track.SavedTrackPaging
   :members:
   :undoc-members:

Audio analysis
**************

.. autoclass:: spotipy.model.audio_analysis.AudioAnalysis
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.audio_analysis.TimeInterval
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.audio_analysis.Section
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.audio_analysis.Segment
   :members:
   :undoc-members:

Audio features
**************

.. autoclass:: spotipy.model.audio_features.AudioFeatures
   :members:
   :undoc-members:


User
----

.. autoclass:: spotipy.model.user.User
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.user.PublicUser
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.user.PrivateUser
   :members:
   :undoc-members:


Miscellaneous
-------------

.. autoclass:: spotipy.model.category.Category
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.category.CategoryPaging
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.context.Context
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.context.ContextType
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.member.Copyright
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.member.Followers
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.member.Image
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.member.Restrictions
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.member.Timestamp
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.recommendations.Recommendations
   :members:
   :undoc-members:

.. autoclass:: spotipy.model.recommendations.RecommendationSeed
   :members:
   :undoc-members:
