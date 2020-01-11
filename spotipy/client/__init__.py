"""
Web API endpoints.

Each method of the client corresponds to an API call, with some exceptions.
Further documentation on endpoints can be viewed in the Web API
`reference <https://developer.spotify.com/documentation/web-api/reference/>`_.

.. code:: python

    from spotipy import Spotify

    # Initialise the client
    spotify = Spotify(token)

    # Call the API
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

Full client
-----------
Client to the Web API.

The full client implements a number of useful methods in addition to
inheriting endpoints of each individual API.

.. currentmodule:: spotipy.client

.. autoclass:: Spotify
   :members:
   :show-inheritance:

   .. automethod:: __init__

.. currentmodule:: spotipy.client.api

Album API
---------
.. autoclass:: SpotifyAlbum
   :members:

Artist API
----------
.. autoclass:: SpotifyArtist
   :members:

Browse API
----------
.. autoclass:: SpotifyBrowse
   :members:
   :inherited-members:

Follow API
----------
.. autoclass:: SpotifyFollow
   :members:

Library API
-----------
.. autoclass:: SpotifyLibrary
   :members:

Personalisation API
-------------------
.. autoclass:: SpotifyPersonalisation
   :members:

Player API
----------
.. autoclass:: SpotifyPlayer
   :members:
   :inherited-members:

Playlist API
------------
.. autoclass:: SpotifyPlaylist
   :members:
   :inherited-members:

Search API
----------
.. autoclass:: SpotifySearch
   :members:

Track API
---------
.. autoclass:: SpotifyTrack
   :members:

User API
--------
.. autoclass:: SpotifyUser
   :members:
"""

from spotipy.client.full import Spotify
