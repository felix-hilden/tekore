.. _models:
.. currentmodule:: tekore.model

Models
======
Response model definitions for :ref:`client <client>`.

Responses are parsed into `Pydantic <https://docs.pydantic.dev/latest/>`_ models.
This allows accessing parts of the response directly as attributes.
Further documentation on specific attribute values can be viewed in the Web API
`reference <https://developer.spotify.com/documentation/web-api/reference/>`_.

.. code:: python

    import tekore as tk

    # Call the API
    spotify = tk.Spotify(token)
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')

    # Use the response
    for track in album.tracks.items:
        print(track.track_number, track.name)

Using Pydantic models means that responses are easy to work with.
They provide a readable ``repr`` (particularly with `devtools
<https://docs.pydantic.dev/latest/usage/devtools/>`_) for quick inspection,
and it is also possible to convert models to builtin and JSON representations:

.. code:: python

    from pprint import pprint

    print(album)
    pprint(album, depth=2)

    album.dict()
    album.json()

Responses will sometimes contain unknown attributes when the API changes.
They are ignored when parsing the response model, but a
:class:`UnknownModelAttributeWarning` is issued when encountering one.
Please consider upgrading Tekore if a newer version documents and handles it.

Models are made available in the :mod:`tekore.models` namespace.

Album
-----
.. autosummary::
   :nosignatures:

   Album
   AlbumGroup
   AlbumType
   SimpleAlbum
   SimpleAlbumPaging
   FullAlbum
   SavedAlbum
   SavedAlbumPaging

.. autoclass:: Album
.. autoclass:: AlbumGroup
   :undoc-members:
.. autoclass:: AlbumType
   :undoc-members:
.. autoclass:: SimpleAlbum
.. autoclass:: SimpleAlbumPaging
.. autoclass:: FullAlbum
.. autoclass:: SavedAlbum
.. autoclass:: SavedAlbumPaging

Artist
------
.. autosummary::
   :nosignatures:

   Artist
   SimpleArtist
   FullArtist
   FullArtistCursorPaging
   FullArtistOffsetPaging

.. autoclass:: Artist
.. autoclass:: SimpleArtist
.. autoclass:: FullArtist
.. autoclass:: FullArtistCursorPaging
.. autoclass:: FullArtistOffsetPaging

Audiobook
---------
.. autosummary::
   :nosignatures:

   Audiobook
   SimpleAudiobook
   SimpleAudiobookPaging
   FullAudiobook
   Author
   Narrator

.. autoclass:: Audiobook
.. autoclass:: SimpleAudiobook
.. autoclass:: SimpleAudiobookPaging
.. autoclass:: FullAudiobook
.. autoclass:: Author
.. autoclass:: Narrator

Category
--------
.. autosummary::
   :nosignatures:

   Category
   CategoryPaging

.. autoclass:: Category
.. autoclass:: CategoryPaging

Chapter
-------
.. autosummary::
   :nosignatures:

   Chapter
   SimpleChapter
   SimpleChapterPaging
   FullChapter

.. autoclass:: Chapter
.. autoclass:: SimpleChapter
.. autoclass:: SimpleChapterPaging
.. autoclass:: FullChapter

Episode
-------
.. autosummary::
   :nosignatures:

   Episode
   SimpleEpisode
   SimpleEpisodePaging
   FullEpisode
   SavedEpisode
   SavedEpisodePaging
   ResumePoint

.. autoclass:: Episode
.. autoclass:: SimpleEpisode
.. autoclass:: SimpleEpisodePaging
.. autoclass:: FullEpisode
.. autoclass:: SavedEpisode
.. autoclass:: SavedEpisodePaging
.. autoclass:: ResumePoint

Playback
--------
.. autosummary::
   :nosignatures:

   CurrentlyPlaying
   CurrentlyPlayingContext
   CurrentlyPlayingType
   Queue
   Device
   DeviceType
   Actions
   Disallows
   PlayerErrorReason
   RepeatState

   PlayHistory
   PlayHistoryCursor
   PlayHistoryPaging
   Context
   ContextType

Currently playing
*****************
.. autoclass:: CurrentlyPlaying
.. autoclass:: CurrentlyPlayingContext
.. autoclass:: CurrentlyPlayingType
   :undoc-members:
.. autoclass:: Queue
.. autoclass:: Device
.. autoclass:: DeviceType
   :undoc-members:
.. autoclass:: Actions
.. autoclass:: Disallows
.. autoclass:: PlayerErrorReason
   :undoc-members:
.. autoclass:: RepeatState
   :undoc-members:

Play history
************
.. autoclass:: PlayHistory
.. autoclass:: PlayHistoryCursor
.. autoclass:: PlayHistoryPaging
.. autoclass:: Context
.. autoclass:: ContextType
   :undoc-members:

Playlist
--------
.. autosummary::
   :nosignatures:

   Playlist
   PlaylistTrack
   PlaylistTrackPaging
   SimplePlaylist
   SimplePlaylistPaging
   FullPlaylist
   FullPlaylistTrack
   FullPlaylistEpisode
   LocalPlaylistTrack
   LocalItem
   LocalAlbum
   LocalArtist
   LocalTrack

.. autoclass:: Playlist
.. autoclass:: PlaylistTrack
.. autoclass:: PlaylistTrackPaging
.. autoclass:: SimplePlaylist
.. autoclass:: SimplePlaylistPaging
.. autoclass:: FullPlaylist
.. autoclass:: FullPlaylistTrack
.. autoclass:: FullPlaylistEpisode

Local items
***********
Some playlists contain locally stored tracks.
They contain mostly `None` values along with empty lists and dictionaries.

.. autoclass:: LocalPlaylistTrack
.. autoclass:: LocalItem
.. autoclass:: LocalAlbum
.. autoclass:: LocalArtist
.. autoclass:: LocalTrack

Recommendation
--------------
.. autosummary::
   :nosignatures:

   Recommendations
   RecommendationSeed
   RecommendationAttribute

.. autoclass:: Recommendations
.. autoclass:: RecommendationSeed
.. autoclass:: RecommendationAttribute
   :undoc-members:

Show
----
.. autosummary::
   :nosignatures:

   Show
   SimpleShow
   SimpleShowPaging
   FullShow
   SavedShow
   SavedShowPaging

.. autoclass:: Show
.. autoclass:: SimpleShow
.. autoclass:: SimpleShowPaging
.. autoclass:: FullShow
.. autoclass:: SavedShow
.. autoclass:: SavedShowPaging

Track
-----
.. autosummary::
   :nosignatures:

   Track
   SimpleTrack
   SimpleTrackPaging
   FullTrack
   FullTrackPaging
   SavedTrack
   SavedTrackPaging
   Tracks
   TrackLink
   Restrictions

   AudioAnalysis
   TimeInterval
   Section
   Segment
   AudioFeatures

.. autoclass:: Track
.. autoclass:: SimpleTrack
.. autoclass:: SimpleTrackPaging
.. autoclass:: FullTrack
.. autoclass:: FullTrackPaging
.. autoclass:: SavedTrack
.. autoclass:: SavedTrackPaging
.. autoclass:: Tracks
.. autoclass:: TrackLink
.. autoclass:: Restrictions

Audio analysis
**************
.. autoclass:: AudioAnalysis
.. autoclass:: TimeInterval
.. autoclass:: Section
.. autoclass:: Segment

Audio features
**************
.. autoclass:: AudioFeatures

User
----
.. autosummary::
   :nosignatures:

   User
   PublicUser
   PrivateUser
   ExplicitContent

.. autoclass:: User
.. autoclass:: PublicUser
.. autoclass:: PrivateUser
.. autoclass:: ExplicitContent

Miscellaneous
-------------
.. autosummary::
   :nosignatures:

   Copyright
   Followers
   Image
   ReleaseDatePrecision

.. autoclass:: Copyright
.. autoclass:: Followers
.. autoclass:: Image
.. autoclass:: ReleaseDatePrecision
   :undoc-members:

Model bases
-----------
.. autosummary::
   :nosignatures:

   Model
   UnknownModelAttributeWarning

   Identifiable
   Item
   Paging
   OffsetPaging
   Cursor
   CursorPaging

Functionality
*************
.. autoclass:: Model
.. autoclass:: UnknownModelAttributeWarning

Models
******
.. autoclass:: Identifiable
.. autoclass:: Item
.. autoclass:: Paging
.. autoclass:: OffsetPaging
.. autoclass:: Cursor
.. autoclass:: CursorPaging

Member types
------------
.. autoclass:: StrEnum
