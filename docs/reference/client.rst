client
======
:class:`Spotify` is a client to the Spotify Web API.
Documentation on its endpoints can be viewed in the
`Web API Reference <https://developer.spotify.com/documentation/web-api/reference/>`_.
Each method of the client corresponds to an API call, with some exceptions.
The full client implements methods from Personalisation, Search and User APIs
in addition to inheriting a number of other APIs documented below.

Full client
-----------

.. autoclass:: spotipy.client.Spotify
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: spotipy.client.Spotify.__init__

Base class
----------

.. autoclass:: spotipy.client.base.SpotifyBase
   :members:
   :undoc-members:

Album API
---------

.. autoclass:: spotipy.client.album.SpotifyAlbum
   :members:
   :undoc-members:


Artist API
----------

.. autoclass:: spotipy.client.artist.SpotifyArtist
   :members:
   :undoc-members:


Browse API
----------

.. autoclass:: spotipy.client.browse.SpotifyBrowse
   :members:
   :undoc-members:


Follow API
----------

.. autoclass:: spotipy.client.follow.SpotifyFollow
   :members:
   :undoc-members:


Library API
-----------

.. autoclass:: spotipy.client.library.SpotifyLibrary
   :members:
   :undoc-members:


Player API
----------

.. autoclass:: spotipy.client.player.SpotifyPlayer
   :members:
   :undoc-members:


Playlist API
------------

.. autoclass:: spotipy.client.playlist.SpotifyPlaylistView
   :members:
   :undoc-members:

.. autoclass:: spotipy.client.playlist.SpotifyPlaylistModify
   :members:
   :undoc-members:

.. autoclass:: spotipy.client.playlist.SpotifyPlaylistTracks
   :members:
   :undoc-members:


Track API
---------

.. autoclass:: spotipy.client.track.SpotifyTrack
   :members:
   :undoc-members:
